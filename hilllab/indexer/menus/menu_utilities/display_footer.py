# Christopher Esther, 1/30/2026

def display_footer(width, line_spacer = '—', ):
    
    # Display bottom bar
    print('\n')
    print(line_spacer * width)

    global_commands = 'mm: main menu, 00: quit'
    print(f'Global: {global_commands}')
    