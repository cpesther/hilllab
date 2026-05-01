# ellen han, 4/23/2026

import matplotlib.pyplot as plt


def performance_dist(metrics, keys, name=None, colors=None):
    """
    makes box plots of some performance metric distribution,
    compare between model types.
    
    ARGUMENTS:
        metrics (tuple): performance metric array (loss, accuracy, pseudo r2),
                         returned by batch_evaluate for model types
        keys (list): the model types (['position','param','summary'])
        
    """
    
    fig, ax = plt.subplots(figsize=(8,6))
    boxplot = ax.boxplot(metrics,
               patch_artist = True,
               tick_labels = [k.capitalize() for k in keys])
    for median in boxplot['medians']:
        median.set_color('black')
    
    if name is not None:
        plt.title(f'{name} Distribution')
        plt.ylabel(name.capitalize())
    
    if colors is not None:

        for i, patch in enumerate(boxplot['boxes']):
            patch.set_facecolor(colors(i)) 
            patch.set_edgecolor('black')

    
    plt.xlabel('Model Type')
    plt.grid(alpha=0.2,axis='y')
    
    plt.show()