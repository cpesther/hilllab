# Christopher Esther, Hill Lab, 10/6/2025

def print_dict_table(dict, title, gap=4, line='-'):

    """
    Prints a dict as a nicely formatted table. 
    """
    
    # Get lengths of each component to calculate spacing
    key_lens = []
    value_lens = []
    for key, value in dict.items():
        key_lens.append(len(str(key)))
        value_lens.append(len(str(value)))
    
    max_key_len = max(key_lens)  # determine maximums
    max_value_len = max(value_lens)
    f_title = f' {title} '
    
    # Determine if a shift is needed
    no_shift_width = max_key_len + max_value_len + gap  # calculate width w/o a shift
    if (no_shift_width - len(f_title)) % 2:  # if odd, add one value for shift
        shift = 1
    else:
        shift = 0
    
    # Calculate the actual width
    f_title = f' {title} '  # title formatted with spacing
    title_width = len(f_title) + 6  # +6 to allow for at least 3 headlines on each side
    data_width = max_key_len + max_value_len + gap + shift
    width = max(title_width, data_width)
    
    # Print the title line
    n_headlines = int((width - len(f_title)) / 2)
    print(f"{line*n_headlines}{f_title}{line*n_headlines}")
    
    # Print the items
    for key, value in dict.items():
        key_buffer = max_key_len - len(str(key))
        value_buffer = max_value_len - len(str(value))
        n_spacing = key_buffer + gap + shift + value_buffer
        print(f"{key}{' '*n_spacing}{value}")
    
    # Print the footer line
    print(f'{line * width}')
    return
