# __init__.py for bead model evaluation subpackage.
# Initializes package-level imports and configuration.

"""
A bunch of functions to evaluate and plot model performance:
    
    load_models
    - load_models: util, loads models into a list.
    
    batch_evaluate
    - batch_evaluate: averages performance metrics across models.
    
    performance_dist
    - performance_dist: box plots of performance metric distributions.
    
    interpolate_roc
    - interpolate_roc: ROC curve with AUC values, interpolated and averaged across models.               
    
    confusion_matrix
    - confusion_matrix: confusion matrix across models, both avg counts and percentages.
    
    ffca
    - pred_ffca: uses model to predict fractional functional ciliated area (FFCA)
                 averaged across models for each plate. TAKES A LONG TIME!
    - plot_ffca: bar graph to plot pred_ffca results across plates.
    
    prediction_map
    - prediction_map: uses a model to make predictions and plot trajectories for beads
                for qualitative validation.

    bead_traj
    - bead_traj: plots simple bead trajectory for classification examples
    
"""