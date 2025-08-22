# Christopher Esther, Hill Lab, 8/21/2025
import string
import pandas as pd
from .Bundle import Bundle
from ._plate_format_extended import _plate_format_extended
from ._plate_remove_overflows import _plate_remove_overflows

def load_file(path, data_type='SPE', extended=False):
    
    """
    Opens a file dialog window to select a data file. Also runs several
    data adjustment functions depending on the type of data loaded. 
    
    ARGUMENTS:
        path (string): a file path to automatically load a file without
            opening a file dialog window.
        data_type (string): Specifies the type model used to collect the 
            data. Options include 'SPE' (default) and 'TEC'.
        extended (bool): controls whether the plate is interpreted as an
            extended or standard layout.

    RETURNS
        bundle (Bundle.Bundle): a bundled object containing the raw data
            and the attributes used for storing results. 
        loaded_data (pandas.DataFrame): the dataframe of loaded data in
            case anybody was to access it directly. 
    """
    
    # Generate the new column names
    new_names = []
    for i in range(24):
        new_names.append(f'Column {i + 1}')
        
    # Use the provided data_type argument to control our loading logic
    try:
        if data_type == 'TEC':  # Tecan Safire II 
            
            try:
                loaded_data = pd.read_excel(path)
            except:
                loaded_data = pd.read_csv(path)
                    
            # Drop the last 20 rows empty of data
            loaded_data = loaded_data.iloc[:-20]
            
            # Rename every column and add and set the index
            loaded_data = loaded_data.set_index('<>')
            loaded_data.columns = new_names
            
            # Drop the header row from each read
            loaded_data = loaded_data.drop(index=['<>'])
            
        elif data_type == 'SPE':  # SpectraMax M2e format
                
            # Read the data from the very weird format it's stored in
            loaded_data = pd.read_csv(path, sep='\t', encoding='utf-16', 
                lineterminator='\r', header=2, skipinitialspace=True)

            # Take just the columns containing data and drop last four rows
            loaded_data = loaded_data.loc[:, [str(i) for i in range(1, 25)]].iloc[:-4]

            # Replace all NaN values with zero
            loaded_data.fillna(0, inplace=True)

            # Remove the one extra spacer row in the n*17th spot for each read
            loaded_data = loaded_data.drop(loaded_data.index[16::17])

            # Rename every column and add and set the index
            loaded_data.columns = new_names
            length = loaded_data.shape[0]
            loaded_data['<>'] = (list(string.ascii_uppercase[:-10]) * int(length / 16))[:length]
            loaded_data = loaded_data.set_index('<>')

        # If the provided data_type doesn't match any known one
        else:
            valid_types = ['TEC', 'SPE']
            print(f'ERROR: Unrecognized data type')
            print(f'       Valid types include {valid_types}')           
            return
    
    except FileNotFoundError:
        print('ERROR: No file was selected')
        return
    
    except UnicodeDecodeError:
        print('ERROR: Unrecognized file type for specified data type')
        return
    
    # Make adjustments for extended data formats
    num_reads = int(loaded_data.shape[0] / 16)
    if extended:
        loaded_data = _plate_format_extended(input_data=loaded_data, num_reads=num_reads)
    
    # Remove overflow values
    loaded_data, overflow_meta = _plate_remove_overflows(input_data=loaded_data)
    num_overflows = overflow_meta.shape[0]
    
    # Display warning message about overflow values (if present)
    if num_overflows > 0:
        print(f'ALERT: {num_overflows} overflow value(s) are present in this data set')

    # Now that we've done all of the loading and calculation, we will
    # create an instance of our Bundle class which will store all of the 
    # data for this functions operation. Using this class makes it much
    # easier to pass the large amount of raw data and results between the
    # many functions that work with them
    bundle = Bundle()

    # Save everything into this bundle object
    bundle.data.path = path
    bundle.data.extended = extended
    bundle.data.num_columns = loaded_data.shape[1]
    bundle.data.num_rows = loaded_data.shape[0]
    bundle.data.num_reads = num_reads
    bundle.data.raw = loaded_data
    bundle.data.overflow_meta = overflow_meta

    # Print a confirmation message
    print('Data sucessfully loaded')
    return bundle
