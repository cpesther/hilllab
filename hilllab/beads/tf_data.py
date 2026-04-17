# ellen han, 3/9/2026

import tensorflow as tf
import pandas as pd
import numpy as np

from .load_hdf import load_hdf

"""
functions to prepare bead datasets for tensorflow:
    
    - param_data: return formatted dataset of a few parameters
    - position_data: return formatted dataset of positions 
    - summary_data: return formatted dataset of all summary
    
    - data_preprocessing: concatenates formatted datasets (if needed)
                        split into train/test/validation datasets
                        shuffle, padded batch, prefetch 
                        
for training: pass path to data and labels to ###_data
              pass that to data_preprocessing
for classify: just pass path to data to ###_data
                        
"""

def param_data(data,labels=None):
    """
    takes a few primary analysis parameters:
        displacement, straightness, circular variance, 
        bounding box area, mean speed, mean acceleration
    and reformats into a tensorflow dataset object. 

    ARGUMENTS:
        data (str): path to h5 file primary analysis data
        labels (str): opt, path to xlsx file bead classifications
        
    RETURNS:
        dataset (tf.data.Dataset): dataset containing param (and label) data
    
    """
    
    # load primary analysis summary
    groupby_summary,*_ = load_hdf(data)
    all_beads = list(groupby_summary.groups.keys()) # list uuid
    
    # dataset for model training
    if labels is not None:
        
        # load bead classification labels
        df_class = pd.read_excel(labels).drop_duplicates(subset='uuid')
        df_class.set_index('uuid', inplace=True) # index by uuid
        
        # filter beads
        uuids = [uuid for uuid in all_beads 
        if uuid in df_class.index 
        and df_class.loc[uuid, 'classification'] != 'idk']
        
        def generator():
            for uuid in uuids:
            
                # get label
                label = df_class.loc[uuid,'classification']
            
                # get params
                bead_data = groupby_summary.get_group(uuid)
                params = bead_data[['displacement','straightness','circular_variance',
                                    'bb_area','mean_speed','mean_acceleration']].values[0]
                
                yield params.astype('float32'), str(label)
                
        output_signature = (
            tf.TensorSpec(shape=(6,), dtype=tf.float32), # param
            tf.TensorSpec(shape=(), dtype=tf.string) # label
            )
    
    # dataset for model use
    else:
        uuids = all_beads
        def generator():
            for uuid in uuids:
                
                # get params
                bead_data = groupby_summary.get_group(uuid)
                params = bead_data[['displacement','straightness','circular_variance',
                                    'bb_area','mean_speed','mean_acceleration']].values[0]
                
                yield params.astype('float32')
                
        output_signature = tf.TensorSpec(shape=(6,), dtype=tf.float32) # param
                
    dataset = tf.data.Dataset.from_generator(generator, output_signature = output_signature)
    count = len(uuids)
    
    return dataset, count

        
def position_data(data,labels=None):
    """
    takes bead x- and y- position data
    and reformats into a tensorflow dataset object.
    
    ARGUMENTS:
        data (str): path to h5 file primary analysis data
        labels (str): opt, path to xlsx file bead classifications
        
    RETURNS:
        dataset(tf.data.Dataset): dataset containing position (and label) data
    
    """
    
    # load primary analysis positions
    groupby_summary,groupby_positions,*_ = load_hdf(data)
    all_beads = list(groupby_summary.groups.keys()) # list uuid
    
    # dataset for model training
    if labels is not None:
        
        # load bead classification labels
        df_class = pd.read_excel(labels).drop_duplicates(subset='uuid')
        df_class.set_index('uuid', inplace=True) # index by uuid
        
        # filter beads
        uuids = [uuid for uuid in all_beads 
        if uuid in df_class.index 
        and df_class.loc[uuid, 'classification'] != 'idk']
    
        def generator():
            for uuid in uuids:
                
                # get label
                label = df_class.loc[uuid,'classification']
                
                # get positions
                bead_positions = groupby_positions.get_group(uuid)
                
                # normalize by mean positions
                bead_summary = groupby_summary.get_group(uuid)
                x_mean = bead_summary['mean_x'].iloc[0]
                y_mean = bead_summary['mean_y'].iloc[0]
                
                x_data = bead_positions['x'] - x_mean
                y_data = bead_positions['y'] - y_mean
                positions = np.stack([x_data,y_data],axis=-1).astype('float32')
    
                yield positions, str(label)
                
        output_signature = (
            tf.TensorSpec(shape=(None,2), dtype=tf.float32), # positions
            tf.TensorSpec(shape=(), dtype=tf.string) # label
            )
    
    # dataset for model use
    else:
        uuids = all_beads
        def generator():
            for uuid in uuids:
                
                # get positions
                bead_positions = groupby_positions.get_group(uuid)
                
                # normalize by mean positions
                bead_summary = groupby_summary.get_group(uuid)
                x_mean = bead_summary['mean_x'].iloc[0]
                y_mean = bead_summary['mean_y'].iloc[0]
                
                x_data = bead_positions['x'] - x_mean
                y_data = bead_positions['y'] - y_mean
                positions = np.stack([x_data,y_data],axis=-1).astype('float32')
    
                yield positions
                
        output_signature = tf.TensorSpec(shape=(None,2), dtype=tf.float32) # positions
                
            
    dataset = tf.data.Dataset.from_generator(generator, output_signature = output_signature)
    count = len(uuids)
    
    return dataset, count


def summary_data(data,labels=None):
    """
    takes every relevant primary analysis parameter (displacement -> bb_area)
    and reformats into a tensorflow dataset object.
    
    ARGUMENTS:
        data (str): path to h5 file primary analysis data
        labels (str): opt, path to xlsx file bead classifications
        
    RETURNS:
        dataset(tf.data.Dataset): dataset containing summary (and label) data
        
    """
    
    # load primary analysis summary
    groupby_summary,*_ = load_hdf(data)
    all_beads = list(groupby_summary.groups.keys()) # list uuid
    
    # dataset for model training
    if labels is not None:
        
        # load bead classification labels
        df_class = pd.read_excel(labels).drop_duplicates(subset='uuid')
        df_class.set_index('uuid', inplace=True) # index by uuid
        
        # filter beads
        uuids = [uuid for uuid in all_beads 
        if uuid in df_class.index 
        and df_class.loc[uuid, 'classification'] != 'idk']
        
    
        def generator():
            for uuid in uuids:

                # get label
                label = df_class.loc[uuid,'classification']
            
                # get params
                # all from displacement to bb area
                bead_data = groupby_summary.get_group(uuid)
                params = bead_data.iloc[:,28:55].values[0] 
                
                yield params.astype('float32'), str(label)
                
        output_signature = (
            tf.TensorSpec(shape=(27,), dtype=tf.float32), # param vector
            tf.TensorSpec(shape=(), dtype=tf.string) # label
            )
        
    # dataset for model use  
    else: 
        uuids = all_beads
        def generator():
            for uuid in uuids:
                
                # get params
                # all from displacement to bb area
                bead_data = groupby_summary.get_group(uuid)
                params = bead_data.iloc[:,28:55].values[0] 
                
                yield params.astype('float32')
                
        output_signature = tf.TensorSpec(shape=(27,), dtype=tf.float32) # param vector
        
    dataset = tf.data.Dataset.from_generator(generator, output_signature = output_signature)
    count = len(uuids)
    
    return dataset, count
   
 
def data_preprocess(datasets):
    """
    preprocesses datasets for tensorflow training:
        concatenates formatted datasets if needed (same features);
        encodes bead classification labels into integer labels;
        splits into training, validation, and test datasets (80/10/10);
        shuffle, padded batch, prefetch.
    returns train, val, test datasets ready to be fed to model
    
    ARGUMENTS:
        datasets: output from ###_data (dataset, count)
                  (if list, must be from same ###_data func)
    
    RETURNS:
        train_ds (tf.data.Dataset): to train the model 
        val_ds (tf.data.Dataset): to validate during training 
        test_ds (tf.data.Dataset): to evaluate after training 
        
    """
    
    # concatenate datasets if multiple
    if isinstance(datasets,list):
        all_ds, total_beads = datasets[0]
        for ds, count in datasets[1:]:
            all_ds = all_ds.concatenate(ds)
            total_beads += count
    else: all_ds, total_beads = datasets
    
    # encode labels to integers
    vocab = ['stuck','transiting','oscillating','discard']
    lookup = tf.keras.layers.StringLookup(vocabulary=vocab, num_oov_indices=0)
    
    @tf.autograph.experimental.do_not_convert
    def encode(features, label_str):
        return features, lookup(label_str)
    
    all_ds = all_ds.map(encode, num_parallel_calls=tf.data.AUTOTUNE)
    
    # shuffle 
    all_ds = all_ds.shuffle(buffer_size=10000, seed=42)
    
    # split into train, val, test
    
    train_size = int(0.8*total_beads) 
    val_size = int(0.1*total_beads)
    
    train_ds = all_ds.take(train_size)
    all_ds = all_ds.skip(train_size)
    
    val_ds = all_ds.take(val_size)
    test_ds = all_ds.skip(val_size)
    
    # padded batch, prefetch
    train_ds = train_ds.cache().padded_batch(32).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.cache().padded_batch(32).prefetch(tf.data.AUTOTUNE)
    test_ds = test_ds.cache().padded_batch(32).prefetch(tf.data.AUTOTUNE)
    
    return train_ds, val_ds, test_ds
  