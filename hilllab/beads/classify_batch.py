# ellen han, 3/9/2026

from pathlib import Path
import pandas as pd
import datetime 
import getpass

from .load_hdf import load_hdf

def classify_batch(path,file,bead_class):
    """
    Assigns all beads in a particular file a motion classification.
    
    ARGUMENTS:
        path (str): path to a .h5 file with bead data
        new (str): path to a .xlsx file to record classifications
        classification (str): classification, must be one of: 
            's': stuck
            't': transiting
            'o': oscillating
    """
    
    class_dict = {
        's':'stuck',
        't':'transiting',
        'o':'oscillating'
        }
    
    if bead_class in class_dict:
        classification = class_dict[bead_class]
    else:
        raise Exception('bead class must be one of: s, t, o')
    
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
    for i,bead_uuid in enumerate(all_beads):
        
        # record information
        output = {
            'index':i,
            'uuid':bead_uuid,
            'classification':classification,
            'timestamp':datetime.datetime.now(),
            'username':username}
        
        outputs.append(output)
      
    # save to excel
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
        
        