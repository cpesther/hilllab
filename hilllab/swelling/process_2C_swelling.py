# Christopher Esther, Hill Lab, 11/13/2025
import pandas as pd
import numpy as np
from pathlib import Path
from openpyxl import load_workbook
import matplotlib.pyplot as plt

from ..swelling._load_file import _load_file
from ..swelling.calculate_NIF import calculate_NIF
from ..utilities.custom_axes import custom_axes

def process_2C_swelling(path, groups=[], time_units='hours', read_sample_interval=12, interval_minutes=15):

    """
    Processes data from a two-channel swelling assay and outputs summarized
    data to an Excel file based on the provided column groups.

    ARGUMENTS:
        path (string): the path to the file to be processed
        groups (dict): a dictionary of group names keyed by the name of the
            group with values of lists of the constituent column numbers
            used for average and standard deviation calculations. 
        time_units (string): 'hours' or 'minutes' controlling the units
            in which the swelling data is displayed
        read_sample_interval (int): the interval to be used for sampling
            the data for export (i.e. save the values every n reads)
        interval_minutes (int): the number of minutes between subsequent
            reads in the dataset. 
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

    # And the index numbers for each read we want to sample
    read_index_numbers = np.arange(0, num_reads - 1, read_sample_interval)

    results = {
        'green': {'mean': {}, 'std': {}},
        'red': {'mean': {}, 'std': {}}
    }

    for group in groups:
        
        name = group
        cols = [f'Column {c}' for c in groups[group]]

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

    # Same for red channel
    blank_col = pd.DataFrame(index=red_mean_df.index, columns=[''])
    red_combined = pd.concat([red_mean_df, blank_col, red_std_df], axis=1)
    multi_cols = (
        [('Mean', col) for col in red_mean_df.columns] +
        [(' ', ' ')] +
        [('STD', col) for col in red_std_df.columns]
    )
    red_combined.columns = pd.MultiIndex.from_tuples(multi_cols)

    # Set the indices to the desired units
    if time_units == 'hours':
        new_index = green_combined.index * interval_minutes * read_sample_interval / 60
    else:
        new_index = green_combined.index * interval_minutes * read_sample_interval

    # Set the new indices and names
    green_combined.index = new_index
    red_combined.index = new_index

    # Export to Excel
    with pd.ExcelWriter(save_path, engine='openpyxl') as writer:
        green_combined.to_excel(writer, sheet_name='Green Channel', index=True)
        red_combined.to_excel(writer, sheet_name='Red Channel', index=True)

    # Multi index columns don't play nice with Excel spaing, so we need to go
    # in and manually delete the erroneously added blank row 3
    wb = load_workbook(save_path)
    for sheet in wb.worksheets:
        sheet.delete_rows(3)
    wb.save(save_path)
    wb.close()

    # Create a couple graphs to go with this data
    for show_error_bars in [False, True]:
        
        # Create custom axes
        fig, ax = custom_axes(xlabel=f'Time ({time_units})', ylabel='Relative %Δ Integrated Fluorescence')

        # Assemble data
        x = green_mean_df.index
        cols = green_mean_df.columns
        offsets = np.linspace(-0.2, 0.2, len(cols))

        for i, col in enumerate(cols):
            ax.errorbar(
                x + offsets[i],
                green_mean_df[col],
                yerr=green_std_df[col] if show_error_bars else None,
                label=col,
                capsize=3,
                marker='o',
                linestyle='-'    )
        
        # Add legend
        ax.legend(loc='upper left', fontsize=14, frameon=False)

        # Save plot
        error_prefix = 'ERROR_' if show_error_bars else ''
        plot_save_path = Path(path).parent / f'PLOT_{error_prefix}{Path(path).stem}.png'
        plt.savefig(plot_save_path, dpi=300)

    print('\nProcessing finished!')
