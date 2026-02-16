# Christopher Esther, Hill Lab, 2/13/2026
import matplotlib.pyplot as plt

def custom_axes(figsize=(8,6), xlabel='', ylabel='', title='', subtitle='',
                log=False, grid=False, grid_ticks='both'):

    # Set default font and create figure and axes
    plt.rcParams.update({'font.family': 'Arial'})
    fig, ax = plt.subplots(figsize=figsize)
    
    # Add gridlines, if requsted
    if grid is True:
        ax.grid(True, which=grid_ticks, linestyle='-', alpha=0.5, 
                color='#dedede')
    elif grid == 'x':
        ax.grid(True, axis=grid, which=grid_ticks, linestyle='-', 
                alpha=0.5, color='#dedede')
    elif grid == 'y':
        ax.grid(True, axis=grid, which=grid_ticks, linestyle='-', 
                alpha=0.5, color='#dedede')
    else:
        pass
        
    # Set tick parameters
    ax.tick_params(which='major', direction='inout', length=15, 
                   labelsize=14, width=2)
    ax.tick_params(which='minor', direction='in', length=5, 
                   labelsize=14, width=1.5)

    # Adjust spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for spine in ['bottom', 'left']:
        ax.spines[spine].set_visible(True)
        ax.spines[spine].set_linewidth(2)

    # Set axis labels
    ax.set_xlabel(xlabel, fontsize=16, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=16, fontweight='bold')

    # Set titles
    fig.suptitle(title, fontsize=18, fontweight='bold')
    ax.set_title(subtitle, fontsize=12)

    # Switch to log scales, if requested
    if log:
        if log in [True, 'xy', 'yx']:
            ax.set_xscale('log')
            ax.set_yscale('log')
        elif log == 'x':
            ax.set_xscale('log')
        elif log == 'y':
            ax.set_yscale('log')
    
    return fig, ax
