# ellen han, 4/23/2026

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from .tf_data import param_data, position_data, summary_data
from .load_hdf import load_hdf


def prediction_map(model, data, key, vocab, interval=None, colors=None):
    """
    makes model predictions on beads from some plate
    plots bead traces, color coded by model-predicted classification.
    
    ARGUMENTS:
        model (tf.keras.Model): a model
        data (str): path to h5 file primary analysis data for some plate
        key (str): model type ('position', 'param,' 'summary')
        interval (tuple): opt, to plot less beads at a time
        
    """
    
    # load data for plot
    groupby_summary,groupby_positions,_,bounds = load_hdf(data)
    all_beads = list(groupby_summary.groups.keys()) # list uuid
    
    # load data for model
    if key =='param':
        plate_ds,_ = param_data(data)
    elif key =='position':
        plate_ds,_ = position_data(data)
    elif key == 'summary':
        plate_ds,_ = summary_data(data)
    else: 
        raise SyntaxError('key must be one of: position, param, summary')
    
    # slice data
    if interval is not None:
        start, end = interval
        uuids = all_beads[start:end]
        plate_ds = plate_ds.skip(start).take(end - start)
    else:
        uuids = all_beads
        
    # get predictions
    plate_ds = plate_ds.padded_batch(32).prefetch(tf.data.AUTOTUNE)
    
    probs = model.predict(plate_ds,verbose=0)
    preds = np.argmax(probs,axis=1)
    
    # loop through each bead and plot
    
    colors=colors if colors is not None else plt.cm.tab10
    colormap = {v: colors(i) for i, v in enumerate(vocab)}
    
    fig,ax = plt.subplots(figsize=(8,6))
    
    for i, uuid in enumerate(uuids):
        
        # bead trajectory
        bead_pos = groupby_positions.get_group(uuid)
        x, y = bead_pos['x'], bead_pos['y']
        
        # color legend
        color = colormap[vocab[preds[i]]]
        
        ax.plot(x, y, color=color)
        
    for label, color in colormap.items():
        plt.plot([], [], color=color, label=label.capitalize())
    ax.legend(loc='upper right')
    
    ax.set(xlabel = 'X Position (pixels)',
           ylabel = 'Y Position (pixels)',
           xlim = (0,bounds['x']),
           ylim = (0,bounds['y']),
           #title = f'{key.capitalize()} Model Predictions',
           aspect = 'equal')


    ax.grid(alpha=0.2)
    
    plt.tight_layout()
    plt.show()