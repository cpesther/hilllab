# ellen han, 4/23/2026

import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from .tf_data import param_data, position_data, summary_data

"""
functions for model to predict ffca and plot results:
- pred_ffca: uses model to predict fractional functional ciliated area (FFCA)
             averaged across models for each plate. TAKES A LONG TIME!
- plot_ffca: bar graph to plot pred_ffca results across plates.

"""

def pred_ffca(path, models, key):
    """
    use models to predict fractional functional ciliated area (FFCA):
        oscillating/(oscillating + stuck).
    predicts ffca for each plate h5 in a folder by averaging across models.
    
    ARGUMENTS:
        path (str): path to folder containing a bunch of plate h5 files
        models (list): list of models
        key (str): model type ('position','parameter','summary')
        
    RETURNS:
        avg_ffca (list): list of avg ffca for each plate
        std_ffca (list): list of ffca std dev for each plate
        labels (list): list of plate name labels
        
    """
    
    plate_map = {}
    
    # load plate h5 files 
    files = [f for f in os.listdir(path) if f.endswith('.h5')]

    # loop over plates
    for file in files:
        plate = os.path.join(path, file)
        
        # reformat plate h5 into tf dataset
        if key =='param':
            plate_ds,_ = param_data(plate)
        elif key =='position':
            plate_ds,_ = position_data(plate)
        elif key == 'summary':
            plate_ds,_ = summary_data(plate)
        else: 
            raise SyntaxError('key must be one of: position, param, summary')
        
        plate_ds = plate_ds.padded_batch(32).prefetch(tf.data.AUTOTUNE)

        # loop over models
        ffcas = [] 
        
        for model in models:
        
            # run model
            probs = model.predict(plate_ds,verbose=0)
            preds = np.argmax(probs,axis=1)
            
            # get predicted osc and stuck
            counts = np.bincount(preds,minlength=4)
            
            stuck = counts[0]
            osc = counts[2]
            
            # calculate ffca from osc stuck proportion
            ffca = osc/(osc+stuck)
            ffcas.append(ffca)
        
        # get plate labels
        name = file.replace('.h5', '').split('_')[0] # combine if same label no.
        if name not in plate_map:
            plate_map[name] = []
        plate_map[name].append(ffcas)
        
    avg_ffca = []
    std_ffca = []
    labels = [] 
    
    # sort labels
    sorted_keys = sorted(plate_map.keys(), key=lambda x: int(x.replace('Plate', '')))

    for label in sorted_keys:
        ffcas = plate_map[label]
        avg_ffca.append(np.mean(ffcas))
        std_ffca.append(np.std(ffcas))
        labels.append(label)   
        
    return avg_ffca, std_ffca, labels
   
         
def plot_ffca(avg_ffca, std_ffca, labels, colors=None):
    """
    plots fractional functional ciliated area (FFCA) bar plot.
    
    ARGUMENTS: 
        pred_ffca (tuple): returned by pred_ffca (avg_ffca, std_ffca, labels) 
        colors (cmap): opt, aesthetics
        
    """

    # genotypes list
    genotypes = ['normal','CCDC39','CCDC39','normal','normal',
                 'CCDC39','CCNO','CCDC39','DNAH11','DNAH11',
                 'normal','unknown','RSPH4A','normal','unknown',
                 'unknown','unknown'] # plate20 not in key so marked as unknown

    # plot
    fig, ax = plt.subplots(figsize=(8,6))
    
    # colors
    colors=colors if colors is not None else plt.cm.tab10
    colormap = {
        'Normal': colors(0),
        'PCD': colors(1),
        'Unknown': colors(2)
    }
    
    bar_colors = []
    for g in genotypes:
        if g == 'normal':
            bar_colors.append(colormap['Normal'])
        elif g == 'unknown':
            bar_colors.append(colormap['Unknown'])
        else:
            bar_colors.append(colormap['PCD'])

    
    plt.bar(labels,avg_ffca,yerr=std_ffca,color=bar_colors)
    
    #legend
    for name, color in colormap.items():
        ax.bar(0, 0, color=color, label=name)
    ax.legend(title='Genotype', loc='upper right')
    
    plt.grid(alpha=0.2,axis='y')
    plt.ylabel('Fractional Functional Ciliated Area')
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()