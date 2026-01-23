# ellen han, 1/14/2026

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import datetime 
import getpass

def classify(path,file,start=0):
    """
    Plots the XY position of beads from a .h5 file. Asks for user input
    classification of motion (stuck, transiting, oscillating) and writes
    or updates a .xlsx file. Bead UUID, classification, and user metadata
    are all saved.
    
    ARGUMENTS:
        path (str): path to a .h5 file with bead data
        new (str): path to a .xlsx file to record classifications
        start (int): index of bead to start from (default to 0)
    """

    username = getpass.getuser()

    # Load bead positions
    df_positions = pd.read_hdf(path, key='/positions')
    df_summary = pd.read_hdf(path, key='/summary')
    
    grouped = df_positions.groupby('uuid') 
    all_beads = list(grouped.groups.keys())
    
    xmax = df_positions['x'].max()
    ymax = df_positions['y'].max()
    
    groupeds = df_summary.groupby('uuid') 
    
    outputs = []
    
    # Loop over beads 
    for i,bead_uuid in enumerate(all_beads[start:],start=start):
        
        bead_data = grouped.get_group(bead_uuid)
        
        time_data = groupeds.get_group(bead_uuid)
        dt = time_data['lifetime_seconds']/time_data['lifetime_frames']
        time = np.arange(0,time_data['lifetime_seconds'].iloc[0],dt.iloc[0])
        
        # Plot bead
        fig = plt.figure(figsize=(18, 8))
        gs = GridSpec(2,2,figure=fig,height_ratios=[2,1])
        fig.suptitle(f'bead {i} | uuid: {bead_uuid}',fontsize=20)
        
        # Plot bead xy zoomed out
        ax1 = fig.add_subplot(gs[:,0])
        ax1.plot(bead_data['x'], bead_data['y'],linewidth=3)
        ax1.set(xlim=(0,xmax),ylim=(0,ymax))
        ax1.set(xlabel='X Position (pixels)', ylabel='Y Position (pixels)',
                aspect='equal')
        
        # Plot bead xy zoomed in
        ax2 = fig.add_subplot(gs[0,1])
        ax2.plot(bead_data['x'], bead_data['y'])
        ax2.set(xlabel='X Position (pixels)', ylabel='Y Position (pixels)')
        
        # Plot bead x vs time
        subgs = gs[1, 1].subgridspec(1,2,wspace=0.2)
        ax3 = fig.add_subplot(subgs[0,0])
        ax3.plot(time, bead_data['x'])
        ax3.set(xlabel='Time (s)', ylabel='X Position (pixels)')

        # Plot bead y vs time
        ax4 = fig.add_subplot(subgs[0,1])
        ax4.plot(time, bead_data['y'])
        ax4.set(xlabel='Time (s)', ylabel='Y Position (pixels)')
        
        plt.tight_layout()
        plt.show()
        
        # Ask for classification
        bead_class = input('Please classify this bead as: \n' 
                           'Stuck (s), Transiting (t), or Oscillating (o)? \n'
                           '(Enter anything else to SKIP.) \n').strip().lower()
        class_dict = {
            's':'stuck',
            't':'transiting',
            'o':'oscillating',
            'i':'idk'}
        
        if bead_class not in class_dict:
            bead_class = 'i'
            print('Unsure; skipped. \n')
        
        classification = class_dict[bead_class]
            
        # Record information
        output = {
            'uuid':bead_uuid,
            'classification':classification,
            'timestamp':datetime.datetime.now(),
            'username':username}
        
        outputs.append(output)

        # Continue or exit
        ok = input('Press ENTER to continue. \n' 
                   'Enter anything else to SAVE AND EXIT. \n')
        if ok:
            print(f'Saving and exiting. You have stopped at: \n'
                  f'Bead index {i}/{(len(all_beads))-1} (uuid: {bead_uuid}). \n')
            break
       
    # Save to Excel  
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
        