# Christopher Esther, Hill Lab, 2/28/2026
import pandas as pd
from pathlib import Path

def _binding_results_handler(results, save=False, save_path=None, save_name=None):

    """
    Helps load and verify results file from the binding assay and also
    extracts certain file metadata information used by other functions.
    Mostly used to help centralize this behavior and avoid having to 
    rewrite file handling code for the many plotting functions that must
    interact with binding results files. 

    ARGUMENTS:
        results (string or pandas.DataFrame): either the path to the binding 
            results file or the results dataframe itself. 
        save (bool): controls whether a specific save folder path for
            this file is generated. 
        save_path (string): a specific path that will be used to save
            any resultant file from this file's processing. Providing
            a value for this argument bypasses automatic save folder
            path generation. 
        save_name (string): used for generating the specific path for 
            saving any resultant files. Mostly used for plotting functions. 

    RETURNS:
        results (pandas.DataFrame): the raw data read directly from the
            Excel file. 
        pivoted (pandas.DataFrame): the results pivoted on the file and
            slide type with the number of expected size beads as the
            value. 
        file (string): the raw file path
        parent (string): the file path to the parent folder of the Excel
            file that was loaded. 
        save_path (string): the
    """

    # Check the type of the results argument and proceed from there
    if type(results) is str:
        file = Path(results)
        parent = file.parent     # calculate parent path
        results = pd.read_excel(results)  # read the file
    
    # Otherwise a file and parent can't be determined if a dataframe
    # was passed directly in
    else:
        file = None
        parent = None
    
    # Pivot the results (useful for plotting)
    pivoted = results.pivot(index='file', columns='slide', values='n_expected')

    # Do a couple extra calculations on the pivot table
    pivoted['total'] = pivoted['bound'] + pivoted['runoff']
    pivoted['% bound'] = pivoted['bound'] / pivoted['total'] * 100
    pivoted['% runoff'] = pivoted['runoff'] / pivoted['total'] * 100

    # Generate the specific save path, if requested
    if save:

        # If a path was provided, use that one
        if save_path is not None:
            save_folder = save_path

        # If not, check if we can create one from the parent path
        elif parent is not None:
            save_folder = parent / 'plots'

        # Otherwise no place to save was provided, so throw an error
        else:
            raise OSError('No save path could be calculated nor was provided')
        
        # Generate the entire save path, if possible
        if save_name:

            # Include file name in save name, if possible
            if file is None:
                save_path = Path(save_folder) / f'{save_name}.png'
            else:
                save_path = Path(save_folder) / f'{save_name}_{Path(file).stem}.png'

            # Ensure the save folder exists
            save_folder.mkdir(parents=True, exist_ok=True)

    return results, pivoted, file, parent, save_path
