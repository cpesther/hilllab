# Christopher Esther, Hill Lab, 1/29/2026
import matplotlib.pyplot as plt
import numpy as np
import os

from ..migration.load_file import load_file

def plate_inspect(bundle=None, path=None, data_type='SPE', extended=False,
                  normalize=False, export=False):

    """
    Generates plots of raw data over time to aid in inspection and
    processing decisions.

    ARGUMENTS:
        bundle (migration.Bundle): data stored in the bundle class 
        path (string): the path to the data to be analyzed if a bundle
            is not provided.
        data_type (string): Specifies the type model used to collect the 
            data. Options include 'SPE' (default), 'TEC', and 'PRE'.
        extended (bool): controls whether the plate is interpreted as an
            extended or standard layout.
        normalize (bool): controls whether the data is normalized before
            plotting
        export (bool): controls whether the inspection plot is 
            exported to a PNG
        
    """

    # Choose data source (bundle or path)
    if (not bundle) and (not path):
        raise ValueError('Either a path or bundle must be provided')

    # If a bundle wasn't provided load the data from a file
    if not bundle:
        bundle = load_file(path=path, data_type=data_type, extended=extended);  # noqa: E703
    
    # Set up the plot, adjust spacing, and calculate the number of reads
    if bundle.data.raw.shape[1] == 32:
        n_rows = 4
        height = 6.66667
    else:
        n_rows = 3
        height = 5
    fig, ax = plt.subplots(n_rows, 8, figsize=(16, height), 
    sharex=True, sharey=True)
    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    num_reads = bundle.data.raw.shape[0] / 16

    # Set the cmap that controls the color change over time
    cmap = plt.get_cmap('viridis')

    # For every column in the raw data
    for index, column in enumerate(bundle.data.raw.columns):
        
        # Determine the coordinates of the approriate plot
        row = index // 8
        col = index % 8

        # Set the y-axis range
        if normalize:
            ax[row, col].set_ylim(0, 1)
        else:
            dataset_max = bundle.data.raw.max().max()
            ax[row, col].set_ylim(0, int(dataset_max))

        # Add the big column number and gridlines
        ax[row, col].text(0.5, 0.5, str(index + 1), 
                    transform=ax[row, col].transAxes, fontsize=40, 
                    color='gray', alpha=0.3, ha='center', va='center')
        ax[row, col].grid(True, color='#dedede')
        ax[row, col].set_xticks(np.arange(0, 15, 2))  # remove x-axis ticks for clarity

        # For every read in the data
        for read in range(int(bundle.data.raw.shape[0] / 16)):

            # Pull and isolate the data
            all_data = bundle._load_read(read, type='raw')
            one_data = all_data[column].to_numpy().astype(int)

            # Normalize the data (if requested)
            if normalize:
                # Add a very small number to prevent any divide by zero errors
                one_data=one_data / (max(one_data) + 1e-10)
        
            # Calculate the color of the line
            color = cmap(read / num_reads)  
            
            # Plot the data
            ax[row, col].plot(one_data, color=color)

        # Add in the overflow indicators
        # Pull just the overflows for that column
        column_overflows = bundle.data.overflow_meta.loc[bundle.data.overflow_meta['Column'] == column]
        read_rows = np.unique(column_overflows['Read Row'].to_numpy())
        
        # Count how many of the reads overflowed for each read index location
        for ovf_row in read_rows:
            num_row_overflows = column_overflows.loc[column_overflows['Read Row'] == ovf_row].shape[0]
            
            # Add the lines to the plot
            ax[row, col].axvline(x=ovf_row, ymax=int(dataset_max), c='red', lw=0.6)

            # And add the number indicators
            y_value = (int(dataset_max) * 0.95) - (int(dataset_max) / 16) * ovf_row
            ax[row, col].text(x=ovf_row, y=y_value, s=f' {num_row_overflows}/{int(bundle.data.num_reads)}', 
                            c='red', fontweight='bold', va='center', fontsize=6)

    # Add a color bar to the right side
    norm = plt.Normalize(vmin=0, vmax=num_reads)
    cbar_ax = fig.add_axes([0.124, 0.02, 0.25, 0.02]) # Position for horizontal color bar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal', label='Read Number')
    cbar.set_ticks([0, num_reads])
    cbar.set_ticklabels(['0', f'{int(num_reads)}'])

    # Add a title and text information
    fig.suptitle(f"{os.path.basename(bundle.data.path).split('.')[0]}", fontweight='bold',
            va='top', y=0.94)

    # Save the inspection figure, if requested
    if export:
        save_name = 'INSPECT_' + os.path.basename(bundle.data.path).split('.')[0] + '.png'
        save_path = os.path.join(os.path.dirname(bundle.data.path), save_name)
        plt.savefig(save_path, dpi=300)
