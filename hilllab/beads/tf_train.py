# ellen han, 3/23/2026

import tensorflow as tf
import keras
from keras import layers
import matplotlib.pyplot as plt
import numpy as np

"""
functions for bead classification model training in tensorflow:
    
    MODELS:
    - param_model: model build for few parameter dataset
    - position_model: model build for position dataset 
    - summary_model: model build for all summary dataset
        
    TRAINING:
    - train: trains model on train dataset
             validates model on val dataset
    
    EVALUATION:
    - evaluate: evaluates model on the unseen test dataset
                    returns accuracy, loss, mcfadden pseudo-r2
                    plots model training history
                    
"""

# 1. build model

def param_model():
    model = keras.Sequential(
        [
            layers.Input(shape=(6,)), # input layer (6,)
            layers.Dense(32, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.5), # prevent overfit
            layers.Dense(4, activation='softmax') # output classes (4)
        ]
    )
    
    return model

def position_model():
    model = keras.Sequential(
        [
            layers.Input(shape=(None,2)), # input layer (None,2)
            layers.Masking(0), # ignore padded batch 0s
            layers.LSTM(64, return_sequences=False), # all traj over time
            layers.Dense(32, activation='relu'),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.5), # prevent overfit
            layers.Dense(4, activation='softmax') # output classes (4)
        ]
    )
    
    return model

def summary_model():
    model = keras.Sequential(
        [
            layers.Input(shape=(27,)), # input layer (27,)
            layers.Dense(128, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.5), # prevent overfit
            layers.Dense(4, activation='softmax') # output classes (4)
        ]
    )
    
    return model


# 2. train model

def train(model, train_ds, val_ds, epochs):
    """
    trains a model for bead classification
    
    ARGUMENTS:
        model (tf.keras.Model): the model to be trained
        train_ds (tf.data.Dataset): training dataset
        val_ds (tf.data.Dataset): validation dataset
        epochs (int): max epochs to train for
                     (earlystop callback is on, so model training stops 
                      automatically when improvement stalls)
        
    RETURNS:
        model (tf.keras.Model): trained model
        history (tf.keras.callbacks.History): history object

    """
    
    # compile model
    # using sparse categorical metrics for integer encoded labels
    model.compile(
        optimizer = 'Adam',
        loss = 'sparse_categorical_crossentropy', 
        metrics = ['sparse_categorical_accuracy'])
    
    # to end training early if model stops getting better
    earlystop = keras.callbacks.EarlyStopping(monitor='sparse_categorical_accuracy', mode='max', patience=3)
    
    # fit model
    history = model.fit(train_ds, 
              epochs=epochs, 
              validation_data=val_ds,
              callbacks=earlystop) 
    
    return model, history
    

# 3. evaluate model

def evaluate(model, test_ds, history=None):
    """
    evaluates model performance on unseen test dataset
    
    ARGUMENTS:
        model (tf.keras.Model): the model to be evaluated
        test_ds (tf.data.Dataset): test dataset
        history (tf.keras.callbacks.History): opt, history object
        
    RETURNS:
        loss (int): sparse categorical crossentropy loss
        accuracy (int): sparse categorical accuracy
        pseudo_r2 (int): mcfadden pseudo r2
            
    """
    
    # performance metrics
    result = model.evaluate(test_ds)
    loss = result[0] # sparse categorical crossentropy loss
    accuracy = result [1] # sparse categorical accuracy
    
    # mcfadden pseudo r2
    # null loss is calculated from sparse categorical crossentropy loss of
    # a prediction matrix based only on label frequency
    labels = []
    for _,label in test_ds.unbatch(): labels.append(label.numpy())
    labels = np.array(labels) # all labels in test dataset
    
    _,counts = np.unique(labels,return_counts=True)
    probs = counts/len(labels) # frequency of each label
    
    preds = np.tile(probs,(len(labels),1)) # frequency prediction matrix
    
    scc = keras.losses.SparseCategoricalCrossentropy() # loss function
    null_loss = scc(labels,preds) # null loss
    
    pseudo_r2 = float(1 - (loss / null_loss)) # pseudo r2
    
    # print metrics
    print(f'test loss: {loss} \n'
          f'test accuracy: {accuracy} \n'
          f'pseudo r2: {pseudo_r2}')
    
    # plot history if provided
    if history is not None:
        
        fig, axs = plt.subplots(1,2,figsize=(12,8))
        fig.suptitle('model history')
        
        axs[0].plot(history.history['sparse_categorical_accuracy'])
        axs[0].plot(history.history['val_sparse_categorical_accuracy'])
        axs[0].legend(['train','test'])
        axs[0].set(title='sparse categorical accuracy',xlabel='epoch',ylabel='accuracy')
        
        # train and val
        axs[1].plot(history.history['loss'])
        axs[1].plot(history.history['val_loss'])
        axs[1].legend(['train','test'])
        axs[1].set(title='sparse categorical crossentropy',xlabel='epoch',ylabel='loss')
        
        plt.tight_layout()
        plt.show()

    return loss, accuracy, pseudo_r2
