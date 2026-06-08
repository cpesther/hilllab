# Christopher Esther, Hill Lab, 5/18/2026
import seaborn as sns
import matplotlib.pyplot as plt

from .parameters import PARAMETERS
from ...utilities.verify_name import verify_name
from .._load_with_groups import _load_with_groups
from ...utilities.custom_axes import custom_axes
from ...utilities.generate_neighbor_path import generate_neighbor_path

def plot_parameter(h5_path, parameter, use_groups=True, save=False, ymax=None, ymin=None):

    """
    Plots one primary analysis parameter as a box and whisker plot. 

    ARGUMENTS:
        h5_path (string): the path to the h5 file to be plotted
        use_groups (bool): if True, data will be categorized using the 
            groups defined in the provided JSON file, if False, data
            will instead be plotted by the identifier column.
        save (bool): if true, figure will be saved to same folder as h5 file
        ymin (int): the minimum value for the y-axis
        ymax (int): the maximum value for the y-axis
    """

    # Verify the parameter first
    valid_parameters = list(PARAMETERS.keys())
    verification = verify_name(name=parameter, valid_names=valid_parameters)

    # Early exit if verification failed
    if not verification:
        return

    # Load the summary data
    summary = _load_with_groups(h5_path, expectations=['identifier'])

    # Set category based on use_groups value
    if use_groups:
        category = 'group'
    else:
        category = 'identifier'

    # Grab the display information about this plot
    parameter_info = PARAMETERS[parameter]
    units_text = f"({parameter_info['units']})" if parameter_info['units'] is not None else None
    parameter_display = f"{parameter_info['display_name']} {units_text}"

    # Gerenate the y label from the 
    # Create the custom axes
    fix, ax = custom_axes(figsize=(11,6), 
                        ylabel=parameter_display, 
                        xlabel=category.capitalize())

    # Create the boxplot for the chosen parameter
    sns.boxplot(data=summary, x=category, y=parameter, hue=category, palette='hsv', 
                legend=False, fliersize=0.4, linecolor='black', linewidth=1.5, ax=ax)

    # Set requested y-axis limits
    ax.set_ylim(ymin, ymax)

    # Save the figure, if requested
    if save:
        
        # Generate the specific prefix based on the arguments
        prefix = f"{parameter.upper()}_"

        # Generate the file path and ensure its save
        final_path = generate_neighbor_path(path=h5_path, extension='.png', 
                                            prefix=prefix, check_safety=True)
        
        # Save the file
        plt.savefig(str(final_path), dpi=400)
