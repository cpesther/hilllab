# Christopher Esther, 1/30/2026
import sys


def ask_option():
    """Used to centralize the behavior for global commands and shortcuts."""

    # Ask user for selection code
    option = input('Selection: ').upper()

    # Return to main menu
    if option == 'MM':
        from ..menu_main import menu_main
        menu_main()

    # End program
    elif option == '00':
        sys.exit(0)

    # If not global option, return code for specific screen to handle
    else:
        return option
    