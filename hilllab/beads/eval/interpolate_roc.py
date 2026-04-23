# ellen han, 4/23/2026

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize


def interpolate_roc(models, vocab, test_ds, name=None, colors=None):
    """
    plots one vs. rest ROC curves with AUC values for each classification.
    ROC curve interpolated and AUC averaged over models.
        
    ARGUMENTS:
        models (list): list of models
        vocab (list): list of classifications (['stuck','transiting','oscillating','discard'])
        test_ds (tf.data.Dataset): test dataset
        
        name (str): opt, label for model name
        colors (cmap): opt, colormap for aesthetics
    
    """
    
    # true labels of test dataset
    true_labels = []
    for _,label in test_ds.unbatch(): true_labels.append(label.numpy())
    true_labels = np.array(true_labels) 
    
    classes = range(len(vocab))
    trues = label_binarize(true_labels,classes=classes)
    
    mean_fpr = np.linspace(0,1,100) # interpolation grid
    
    fig, ax = plt.subplots(figsize=(8,6))
    
    # loop through each class
    for n in classes:
        tprs = []
        aucs = []
       
       # loop through each model
        for model in models:
            
            preds = model.predict(test_ds,verbose=0)
             
            fpr,tpr,_ = roc_curve(trues[:,n],preds[:,n])
            roc_auc = auc(fpr,tpr)
             
            roc_tpr = np.interp(mean_fpr,fpr,tpr)
            roc_tpr[0] = 0
             
            tprs.append(roc_tpr)
            aucs.append(roc_auc)
            
            
        # interpolate roc curve
        mean_tpr = np.mean(tprs,axis=0)
        mean_tpr[-1] = 1
        mean_auc = auc(mean_fpr,mean_tpr)
        std_auc = np.std(aucs)
        
        color = colors(n) if colors is not None else None
    
        plt.plot(mean_fpr,mean_tpr,color=color,lw=2,
                 label=f'{vocab[n].capitalize()} (AUC = {mean_auc:.2f} ± {std_auc:.2f}')
    
    plt.plot([0,1],[0,1],linestyle='--',color='gray')
    
    if name is not None:
        plt.title(f'{name.capitalize()} Model OvR ROC Curves')
        plt.ylabel(name.capitalize())
    
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    
    plt.legend()
    plt.show()
