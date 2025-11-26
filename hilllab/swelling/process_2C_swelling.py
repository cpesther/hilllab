# Christopher Esther, Hill Lab, 11/13/2025
import pandas as pd
import numpy as np
from pathlib import Path

# This try/except allows the function to run in a non-Jupyter environment
try:
    from IPython.display import clear_output
except:
    pass

from ..swelling._load_file import _load_file
from ..swelling.calculate_NIF import calculate_NIF

def process_2C_swelling(path, read_sample_interval, column_groups=[]):

    """
    Processes data from a two-channel swelling assay and outputs summarized
    data to an Excel file based on the provided column groups.

    ARGUMENTS:
        path (string): the path to the file to be processed
        read_sample_interval (int): the interval to be used for sampling
            the data for export (i.e. save the values every n reads)
        column_groups (nested list): a list of lists grouping the columns
            for average and standard deviation calculations. 
    """

    # Load the data
    green_data, red_data, num_reads = _load_file(path=path)
    
    print('Loading green channel...')
    green_integrals = calculate_NIF(green_data, num_reads=num_reads)
    print('\nLoading red channel...')
    red_integrals = calculate_NIF(red_data, num_reads=num_reads)

    # Define and use a helper function to normalize the data based on the 
    # change since the first value
    def _delta_normalize_columns(data):
        norm_df = pd.DataFrame(columns=data.columns)
    
        for column in data.columns:
            raw_data = data[column]
            norm_column = raw_data / raw_data[0]
            norm_df[column] = norm_column
        return norm_df
    
    ngreen_integrals = _delta_normalize_columns(green_integrals)
    nred_integrals = _delta_normalize_columns(red_integrals)
    
    # Prepare a few things before we go through and calculate the averages
    group_names = []  # generate group names for each column group
    for index, group in enumerate(column_groups):
        group_names.append(f'Group {index + 1}')
    
    # And the index numbers for each read we want to sample
    read_index_numbers = np.arange(0, num_reads, read_sample_interval)
    
    results = {
        'green': {'mean': {}, 'std': {}},
        'red': {'mean': {}, 'std': {}}
    }
    
    for gindex, group in enumerate(column_groups):
        name = group_names[gindex]
        cols = [f'Column {c}' for c in group]
    
        g_mean = ngreen_integrals[cols].mean(axis=1)
        g_std = ngreen_integrals[cols].std(axis=1)
        r_mean = nred_integrals[cols].mean(axis=1)
        r_std = nred_integrals[cols].std(axis=1)
    
        idx = read_index_numbers
        results['green']['mean'][name] = g_mean.iloc[idx].tolist()
        results['green']['std'][name] = g_std.iloc[idx].tolist()
        results['red']['mean'][name] = r_mean.iloc[idx].tolist()
        results['red']['std'][name] = r_std.iloc[idx].tolist()

    # Convert nested dicts to DataFrames
    green_mean_df = pd.DataFrame(results['green']['mean'])
    green_std_df = pd.DataFrame(results['green']['std'])
    red_mean_df = pd.DataFrame(results['red']['mean'])
    red_std_df = pd.DataFrame(results['red']['std'])
    
    # Generate the save path for this file
    new_name = f"RESULT {Path(path).name.split('.')[0]}.xlsx"
    save_path = Path(path).parent / Path(new_name)
    
    # Export to Excel with side-by-side tables
    # Create a blank column for spacing
    blank_col = pd.DataFrame(index=green_mean_df.index, columns=['_'])
    
    # Create MultiIndex columns for Mean and STD
    green_combined = pd.concat([green_mean_df, blank_col, green_std_df], axis=1)
    multi_cols = (
        [( 'Mean', col) for col in green_mean_df.columns] +
        [(' ', ' ')] +  # blank column
        [('STD', col) for col in green_std_df.columns]
    )
    green_combined.columns = pd.MultiIndex.from_tuples(multi_cols)
    
    # Same for Red channel
    blank_col = pd.DataFrame(index=red_mean_df.index, columns=[''])
    red_combined = pd.concat([red_mean_df, blank_col, red_std_df], axis=1)
    multi_cols = (
        [('Mean', col) for col in red_mean_df.columns] +
        [(' ', ' ')] +
        [('STD', col) for col in red_std_df.columns]
    )
    red_combined.columns = pd.MultiIndex.from_tuples(multi_cols)
    
    # Export to Excel
    with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
        green_combined.to_excel(writer, sheet_name='Green Channel', index=True)
        red_combined.to_excel(writer, sheet_name='Red Channel', index=True)

    try:
        clear_output(wait=True)
    except:
        pass
    print('Processing finished!')
