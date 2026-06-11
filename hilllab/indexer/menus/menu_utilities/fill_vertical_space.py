# Christopher Esther, 2/21/2026
from ..config import HEADER_HEIGHT, FOOTER_HEIGHT, HEIGHT

def fill_vertical_space(lines_occupied, count_header=True, count_footer=True):

    """
    Adds in a requested number of lines of line breaks to fill vertical space
    """

    # Account for header and footer, if requested
    if count_header:
        lines_occupied += HEADER_HEIGHT
    if count_footer:
        lines_occupied += FOOTER_HEIGHT
        
    # Calculate number of lines to fill
    fill_lines = HEIGHT - lines_occupied
    print(f'fill vertical {fill_lines}')
    # Print blank lines
    for i in range(fill_lines):
        print('\n ')
