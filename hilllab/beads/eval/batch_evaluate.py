# ellen han, 4/20/2026

import numpy as np

from .tf_train import evaluate

def batch_evaluate(models, test_ds):
    """
    averages model performance across models on unseen test dataset.
    
    ARGUMENTS:
        models (tuple): list of models 
        test_ds (tf.data.Dataset): test dataset
        
    RETURNS:
        loss (arr): sparse categorical crossentropy loss array
        accuracy (arr): sparse categorical accuracy array
        pseudo_r2 (arr): mcfadden pseudo r2 array
    
    """
    
    loss = []
    accuracy = []
    pseudo_r2 = []
    
    # evaluate each model
    for model in models:
        
        los, acc, r2 = evaluate(model,test_ds)

        loss.append(los) 
        accuracy.append(acc) 
        pseudo_r2.append(r2)
    
    # average model metrics
    avg_loss = np.mean(loss)
    std_loss = np.std(loss)
    
    avg_acc = np.mean(accuracy)
    std_acc = np.std(accuracy)
    
    avg_r2 = np.mean(pseudo_r2)
    std_r2 = np.std(pseudo_r2)
    
    # print metrics
    print('average model performance \n'
          f'loss: {avg_loss} ± {std_loss} \n'
          f'accuracy: {avg_acc} ± {std_acc} \n'
          f'pseudo r2: {avg_r2} ± {std_r2}')
    
    return loss, accuracy, pseudo_r2