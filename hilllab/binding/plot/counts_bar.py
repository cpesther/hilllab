# Christopher Esther, Hill Lab, 2/28/2026
import seaborn as sns
import matplotlib.pyplot as plt

from ._binding_results_handler import _binding_results_handler
from ...utilities.custom_axes import custom_axes

def counts_bar(results, save=False, save_path=None):

    """
    Creates a paired bar chart of the number of runoff and bound beads
    per well/image for a group of images. 

    ARGUMENTS:
        results (string or pandas.DataFrame): either a string as the
            path to a pre-exported binding results Excel file or the 
            loaded DataFrame containing those results. 
        save (bool): whether the figure produced should be saved as a PNG
        save_path (bool): allows for a specific save path to be provided, 
            otherwise the image will be saved to a plots folder in the
            same directory as the results file. If the results were loaded
            directly from a dataframe, then this argument will be
            required in order to save the plot as an image. 
    """

    # Handle the results
    results, pivoted, file, parent, save_path = _binding_results_handler(results=results, 
                                                                        save=save, save_name='counts_bar')

    # Bar plot bound versus runoff 
    bvr_fig, bvr_ax = custom_axes(figsize=(12, 7), xlabel='Well', ylabel='# Beads', 
                                title='Runoff and Bound per Well', subtitle=file)

    # Create bar chart
    sns.barplot(data=results, x='file', y='n_expected', hue='slide', palette='bright', 
                linewidth=1.5, edgecolor='black', ax=bvr_ax)

    # Add legend
    bvr_ax.legend(loc='upper right', fontsize=14, frameon=False)
    
    # Save the plot, if requested
    if save:
        plt.savefig(save_path, bbox_inches='tight', pad_inches=0.5, dpi=300)
        print(f'Plot saved to {save_path}')
        plt.close()
        