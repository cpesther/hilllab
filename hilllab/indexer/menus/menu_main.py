# Christopher Esther, 1/30/2026
from .config import WIDTH
from . import menu_utilities as menu

def menu_main():

    """
    The main menu. 
    """

    # Display the header
    menu.display_header(title='Main Menu', width=WIDTH)

    # Variable for counting used lines (for filling the blank ones later)
    n_lines = 0

    # Display the options
    options = ['start recording', 'stop recording', 'browse motion', 'search motion by date']
    disp_n_lines, _ = menu.display_options(options=options)
    n_lines += disp_n_lines

    # Fill remaining vertical space
    #fill_vertical_space(lines_occupied=n_lines)

    # Display the footer
    menu.display_footer(width=WIDTH)

    # Ask for selection
    selection = menu.ask_option()

    # Handle selection
    if selection == '1':
        pass
        # go to start recording
    elif selection == '2':
        pass
        # go to stop recording
    elif selection == '3':  # browse motion 
        pass
    else:
        pass

# Run as script
if __name__ == '__main__':

    menu_main()
    