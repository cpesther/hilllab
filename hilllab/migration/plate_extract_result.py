# Christopher Esther, Hill Lab, 2/5/2026
import numpy as np

def plate_extract_result(bundle, column, table, value, end_only=False, end_hours=8):

    """
    Pulls the specified statistical value from the table for the
    specified column.

    ARGUMENTS:
        results (migration.Bundle):
        table (string): one of 'eta', 'D', eta_calib', 'D_calib', 'Dt', '
            nrmse', or 'peak'
        value (string): the statistical value to return. One of 'mean', 
            'median', 'weighted_mean', 'minimum', 'maximum'. 

    RETURNS
        output (float): the requested output value
    """

    valid_tables = ['eta', 'D', 'eta_calib', 'D_calib', 'Dt', 'nrmse', 'peak']
    if table not in valid_tables:
        raise ValueError(f"Table '{table}' is not valid.")

    # First pull the table that the results will be taken from
    selected_table = getattr(bundle.results, f'plate_{table}')

    # If only calculating the parameter on the ending portion of the dataset
    if end_only:
        
        # Calculate the number of reads at the end
        n_reads_included = int(end_hours * 60 / bundle.data.interval_minutes)
        if n_reads_included >= bundle.data.num_reads:
            raise ValueError(f'End range {n_reads_included} is greater than the number of reads in the data ({bundle.data.num_reads}).')

        # Trim the column to this value
        start_index = bundle.data.num_reads - n_reads_included
        selected_column = selected_table[f'Column {column}'][start_index:bundle.data.num_reads]
        nrmse_values = bundle.results.plate_eta[f'Column {column}'][start_index:bundle.data.num_reads]

    # Otherwise, if not taking only end range, just pull the full column
    else:
        selected_column = selected_table[f'Column {column}']
        nrmse_values = bundle.results.plate_eta[f'Column {column}']

    # Calculate the requested value
    if value == 'mean':
        output = np.mean(selected_column)
    elif value == 'median':
        output = np.median(selected_column)
    elif value == 'weighted_mean':
        output = np.average(selected_column, weights=nrmse_values)
    elif value == 'maximum':
        output = max(selected_column)
    elif value == 'minimum':
        output = min(selected_column)
    else:
        raise ValueError(f"Value '{value}' is not valid.")

    return output
