# ellen han, 1/14/2026

from pathlib import Path
import pandas as pd
import datetime 
import getpass

from load_hdf import load_hdf
from plot_bead import plot_bead

def classify_bead(path,file,start=0):
    """
    Plots individual bead trajectory from a HDF file and asks for user-input
    classification of motion (stuck, transiting, oscillating). Writes or updates
    an Excel file with the output. Bead UUID, classification, and user metadata
    are all saved.
    
    ARGUMENTS:
        path (str): path to a .h5 file with bead data
        new (str): path to a .xlsx file to record classifications
        start (int): index of bead to start from (default to 0)
    """

    # get user
    username = getpass.getuser()

    # load data
    groupby = load_hdf(path)
    groupby_summary,*_ = groupby
    
    # to iterate over
    all_beads = list(groupby_summary.groups.keys()) 
    
    # to record 
    outputs = []
    
    # loop over beads 
    for i,bead_uuid in enumerate(all_beads[start:],start=start):
        
        # plot bead
        try:
            plot_bead(bead_uuid, groupby=groupby, pixel_width=1) # pixels or microns
        # save data in case of error
        except Exception: 
            print('Error. Your data will be saved. You have stopped at: \n'
                  f'Bead index {i}/{(len(all_beads))-1} (uuid: {bead_uuid}). \n')
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
        
        if bead_class not in class_dict:
            bead_class = 'i'
            print('Skipped. \n')
        
        classification = class_dict[bead_class]
            
        # record information
        output = {
            'index':i,
            'uuid':bead_uuid,
            'classification':classification,
            'timestamp':datetime.datetime.now(),
            'username':username}
        
        outputs.append(output)

        # continue or exit
        ok = input('Press ENTER to continue. \n' 
                   'Enter anything else to SAVE AND EXIT. \n')
        if ok:
            print(f'You have stopped at: Bead index {i}/{(len(all_beads))-1}.\n'
                  f'(uuid: {bead_uuid}). \n')
            break
       
    # save to Excel 
    if outputs:
        df_new = pd.DataFrame(outputs)
        
        file_path = Path(file)
        
        if file_path.exists():
            df_old = pd.read_excel(file_path)
            df_fin = pd.concat([df_old,df_new],ignore_index=True)
        else:
            df_fin = df_new
            
        df_fin.to_excel(file_path,index=False)
        
        print(f'Saved {len(df_new)} row(s) to {file_path}.')
        
    else:
        print ('Nothing to save.')
        