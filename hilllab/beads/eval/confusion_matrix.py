# ellen han, 4/23/2026

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


def conf_matrix(models, vocab, test_ds):
    """
    plots confusion matrix over models, for both avg counts and avg percentages.
    
    ARGUMENTS:
        models (list): list of models
        vocab (list): list of classifications (['stuck','transiting','oscillating','discard'])
        test_ds (tf.data.Dataset): test dataset
        
    """

    # true labels of test dataset
    trues = []
    for _,label in test_ds.unbatch(): trues.append(label.numpy())
    trues = np.array(trues) 
    
    classes = range(len(vocab))
    
    # generate confusion matrix for each model
    cms = []
    
    for model in models:
        
        probs = model.predict(test_ds,verbose=0)
        preds = np.argmax(probs,axis=1)
        
        cm = confusion_matrix(trues,preds,labels=classes)
        
        cms.append(cm)
    
    # avg matrices
    avg_cm = np.mean(cms,axis=0)
    
    # to get percentages
    row_sums = avg_cm.sum(axis=1)[:, np.newaxis]
    norm_cm = np.divide(avg_cm, row_sums, out=np.zeros_like(avg_cm), where=row_sums!=0)


    #plot me
    fig,(ax1,ax2) = plt.subplots(2, 1, figsize=(5,8))

    disp1 = ConfusionMatrixDisplay(confusion_matrix=avg_cm,display_labels=vocab)
    disp1.plot(cmap=plt.cm.Blues, values_format='.1f', ax=ax1)
    ax1.set_title('Average Counts')
    
    disp2 = ConfusionMatrixDisplay(confusion_matrix=norm_cm,display_labels=vocab)
    disp2.plot(cmap=plt.cm.Blues, values_format='.2f', ax=ax2)
    ax2.set_title('Average Percentages')

    plt.tight_layout()
    plt.show()
