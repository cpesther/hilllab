# ellen han, 3/2/2026

import pandas as pd
import datetime 
import getpass

from load_hdf import load_hdf
from plot_bead import plot_bead

def classify_review(path,file,label='idk',start=0):
    """
    Overwrites bead classifications, iterating through all beads of a
    particular classification. 
    
    ARGUMENTS:
        path (str): path to a .h5 file with bead trajectory data and uuid
        file (str): path to a .xlsx file with classifications and uuid
        label (str): bead class to review (default to 'idk')
        start (int): index of bead to start from (default to 0)
    """
    
    # get user
    username = getpass.getuser()

    # load data
    groupby = load_hdf(path)
    groupby_summary,*_ = groupby
    
    # every bead of label
    df_class = pd.read_excel(file)
    df_some = df_class[df_class['classification'] == label]
    some_beads = df_some['uuid'].tolist()
    
    print(f'Found {len(some_beads)} beads labeled {label}.')
    
    # iterate over these beads
    for i,bead_uuid in enumerate(some_beads[start:],start=start):
        
        # plot bead
        try:
            plot_bead(bead_uuid, groupby=groupby, pixel_width=1) # pixels or microns
        # save data in case of error
        except Exception: 
            print('Error. Your data will be saved. You have stopped at: \n'
                  f'Bead index {i}/{(len(some_beads))-1} (uuid: {bead_uuid}). \n')
            break
        
        # ask for classification
        bead_class = input('Please classify this bead as: \n' 
                           'Stuck (s), Transiting (t), or Oscillating (o)? \n'
                           '(Enter d to DISCARD, or anything else to SKIP.) \n').strip().lower()
        class_dict = {
            's':'stuck',
            't':'transiting',
            'o':'oscillating',
            'i':'idk',
            'd':'discard'}
        
        if bead_class in class_dict:
            classification = class_dict[bead_class]
            
            # overwrite
            mask = df_class['uuid'] == bead_uuid # boolean
            df_class.loc[mask, 'classification'] = classification
            df_class.loc[mask, 'timestamp'] = datetime.datetime.now()
            df_class.loc[mask, 'username'] = username   
        
        else:
            print('Skipped. \n')
            
        # continue or exit
        ok = input('Press ENTER to continue. \n' 
                   'Enter anything else to SAVE AND EXIT. \n')
        if ok:
            print(f'You have stopped at: Bead index {i}/{(len(some_beads))-1}.\n'
                  f'(uuid: {bead_uuid}). \n')
            break
        
        # save updates
        df_class.to_excel(file, index=False)
        print(f'Saved {len(df_class)} row(s) to {file}.')
    