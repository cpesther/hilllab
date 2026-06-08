# Christopher Esther, Hill Lab, 5/4/2026
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .._load_with_groups import _load_with_groups
from ...utilities.custom_axes import custom_axes
from ...utilities.generate_neighbor_path import generate_neighbor_path

def bead_counts(h5_path, cumulative=False, use_groups=True, save=False, ymin=None, ymax=None):

    """
    Plots the number of beads in each category, either as a cumulative
    count or the average per video. 

    ARGUMENTS:
        h5_path (string): the path to the h5 file to be plotted
        cumulative (bool): if true, the cumulative total of beads in each
            category will be plotted as opposed to the average per video.
        use_groups (bool): if True, data will be categorized using the 
            groups defined in the provided JSON file, if False, data
            will instead be plotted by the identifier column.
        save (bool): if true, figure will be saved to same folder as h5 file
        ymin (int): the minimum value for the y-axis
        ymax (int): the maximum value for the y-axis
    """

    # Load the summary data
    summary = _load_with_groups(h5_path, expectations=['identifier'])

    # Set category based on use_groups value
    if use_groups:
        category = 'group'
    else:
        category = 'identifier'

    # Count number of beads in each file
    bead_counts = summary.groupby([category, 'path'])['particle_id'].nunique().reset_index()
    bead_counts.rename(columns={'particle_id': 'bead_count'}, inplace=True)

    # Determine whether we're doing a cumulative or average count
    if cumulative:

        # Calculate cumulative bead counts
        totaldfs = []
        for plate in np.unique(bead_counts[category]):
            platedata = bead_counts[bead_counts[category] == plate]
            total = np.sum(platedata['bead_count'])
            newdf = pd.DataFrame({category: [plate],
                                'total': [total]})
            totaldfs.append(newdf)
        total_counts = pd.concat(totaldfs)

        # Create the custom axes
        fix, ax = custom_axes(figsize=(11,6), 
                              ylabel='Cumulative Bead Count', 
                              xlabel=category.capitalize())

        # Create the bar plot
        sns.barplot(
            data=total_counts,
            x=category,
            y='total',
            hue=category,
            palette='winter',
            zorder=0,
            ax=ax
        )

        # Adjust y axes
        ax.set_ylim(ymin, ymax)

    # If not plotting cumulatively, calulate the averages per file
    else:
        

        # Create the custom axes for the figure
        fix, ax = custom_axes(figsize=(11,6), 
                                ylabel='Average Bead Count (per video)', 
                                xlabel=category.capitalize())

        # Create the actual box plot
        sns.boxplot(
            data=bead_counts,
            x=category,
            y='bead_count',
            hue=category,
            palette='winter',
            ax=ax
        )

        # Some minor adjustments
        ax.set_ylim(ymin, ymax)
        ax.legend().remove()

    # Save the figure, if requested
    if save:
        
        # Generate the specific prefix based on the arguments
        prefix = f"{'TOTAL' if cumulative else 'AVG'} BEAD COUNT_"

        # Generate the file path and ensure its save
        final_path = generate_neighbor_path(path=h5_path, extension='.png', 
                                            prefix=prefix, check_safety=True)
        
        # Save the file
        plt.savefig(str(final_path), dpi=400)
