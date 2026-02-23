# Christopher Esther, Hill Lab, 2/23/2026
import string

def format_spectra_table(t):

    """
    Used to clean up and format a table with 1D diffusion-like data 
    as collected by the SpectraMax plate reader. 
    """

    # Generate new names for the columns
    new_names = []
    for i in range(24):
        new_names.append(f'Column {i + 1}')

    # Replace all NaN values with zero
    t.fillna(0, inplace=True)

    # Remove the one extra spacer row in the n*17th spot for each read
    t = t.drop(t.index[16::17])

    # Rename every column and add and set the index
    t.columns = new_names
    length = t.shape[0]
    t['<>'] = (list(string.ascii_uppercase[:-10]) * int(length / 16))[:length]
    t = t.set_index('<>')
    return t