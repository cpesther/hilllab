# Christopher Esther, Hill Lab, 2/28/2026
import seaborn as sns
import matplotlib.pyplot as plt

from ._binding_results_handler import _binding_results_handler
from ...utilities.custom_axes import custom_axes

def percentage_bar(results, slide, save=False, save_path=None):

    """
    Creates a bar chart of the percentage of runoff, bound, or runoff and 
    bound beads per well/image for a group of images. 

    ARGUMENTS:
        results (string or pandas.DataFrame): either a string as the
            path to a pre-exported binding results Excel file or the 
            loaded DataFrame containing those results. 
        slide (string): one of 'bound', 'runoff', or 'both'. Contols
            which percentages are plotted on the graph. 
        save (bool): whether the figure produced should be saved as a PNG
        save_path (bool): allows for a specific save path to be provided, 
            otherwise the image will be saved to a plots folder in the
            same directory as the results file. If the results were loaded
            directly from a dataframe, then this argument will be
            required in order to save the plot as an image. 

    """

    # Handle the results
    results, pivoted, file, _, save_path = _binding_results_handler(results=results, 
                                                                    save=save, save_name='percentage_bar')

    # Plotting both requires a bit of a different data structure
    if slide.upper() == 'BOTH':

        # Iterate over every row in the results table to calculate the percentage
        # while still maintaining the structure with slide type as a column which
        # is needed for the dual bar chart style. 
        percentages = []
        for _, results_row in results.iterrows():
        
            # Get the total number of beads between runoff and bound from pivot table
            total = pivoted.loc[results_row.file]['total']
        
            # Calculate and append the percentage 
            percentages.append(results_row.n_expected / total * 100)
        
        # Add this percentages row into the dataframe
        results['percentage'] = percentages

        # Bar plot bound versus runoff 
        bvr_fig, bvr_ax = custom_axes(figsize=(12, 7), xlabel='Well', ylabel='%', 
                                      title='% Runoff vs Bound per Well', subtitle=file)
        
        # Create bar chart
        sns.barplot(data=results, x='file', y='percentage', hue='slide', palette='bright', 
                    linewidth=1.5, edgecolor='black', ax=bvr_ax)

        # Add a legend
        bvr_ax.legend(loc='upper right', fontsize=14, frameon=False)

    # Otherwise, assume we are only plotting either bound or runoff
    else:

        # Determine appearance depending on plotting bound or runoff beads
        if slide.upper() == 'BOUND':
            color = '#D28239'
        
        elif slide.upper() == 'RUNOFF':
            color = '#2E4ED7'
        
        else:
            raise ValueError(f"'{slide}' is an unknow value for slide")
        
        # Bar plot bound versus runoff 
        bvr_fig, bvr_ax = custom_axes(figsize=(12, 7), xlabel='Well', ylabel='% Bound', 
                                    title=f'% {slide.capitalize()} per Well', subtitle=file)
        
        # Create bar chart
        sns.barplot(data=pivoted, x='file', y=f'% {slide.lower()}', color=color, 
                    linewidth=1.5, edgecolor='black', ax=bvr_ax)
        
    # Set Y axis limits from 0 to 100
    bvr_ax.set_ylim(0, 100)

    # Save the plot, if requested
    if save:
        plt.savefig(save_path, bbox_inches='tight', pad_inches=0.5, dpi=300)
        print(f'Plot saved to {save_path}')
        plt.close()
