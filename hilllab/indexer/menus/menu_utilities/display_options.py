# Christopher Esther, 1/30/2026

def display_options(options):

    # Print the options
    options_dict = {}
    for i, option in enumerate(options):
        print(f'  [{i + 1}] {option.title()}')
        options_dict[i + 1] = option

    # Calculate number of lines
    n_lines = len(options)

    return n_lines, options_dict
