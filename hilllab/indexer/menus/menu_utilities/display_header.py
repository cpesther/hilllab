# Christopher Esther, 1/30/2026
from ..menu_utilities.clear_terminal import clear_terminal

def display_header(title, width, line_spacer = '—'):
    
    # Clear everything else from termianl
    clear_terminal()

    # Calculate length of title plus space on either side (+2)
    title_length = len(title) + 2
    left_spacer_length = (width - title_length) // 2
    right_spacer_length = width - left_spacer_length - title_length

    # Print the title bar
    title_bar = f'{line_spacer * left_spacer_length} {title.upper()} {line_spacer * right_spacer_length}'
    print(title_bar)

    # Print instructions message
    print('Select an option and press ENTER\n')
