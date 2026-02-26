# Christopher Esther, Hill Lab, 2/26/2026

def _parameter_window_text(parameters='all'):

    """
    Just a simple helper function to keep super long instructions text
    strings out of the main file. 

    ARGUMENTS:
        parameters (string): the parameters values passed to the 
            _parameter_window function, which controls which version
            of the instructions text is returned.

    RETURNS:
        inst (string): the string of instructions text for the 
            _paramter_window GUI. 
    """

    if (parameters == 'all') or (parameters == 'groups'):
        inst = 'Create groups of capillaries by inputting a name and assigning slot numbers. ' \
               'Groups are used when combining multiple data sets, performing statistical analysis, ' \
               'and generating reports. You can create up to 15 unique groups. Hover over each ' \
               'header for tooltips.'
        
    elif parameters == 'radii':
        inst = 'Assign radius values to certain ranges or specific columns. Radii values are always ' \
               'processed in nanometers. Hover over each header for tooltips.'
    
    elif parameters == 'calibration':
        inst = 'Assign eta values to certain ranges or specific columns. These columns are used to ' \
               'calibrate the results of other columns with matching radii values. Eta values should be ' \
               'reported in mPa•s. Hover over each header for tooltips.'
        
    else:
        raise ValueError(f"'{parameters}' is not a valid parameters value.")
    
    # Return the text
    return inst
