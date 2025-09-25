# Christopher Esther, Hill Lab, 8/21/2025
from datetime import datetime
import string
import pandas as pd
from .Bundle import Bundle
from ._plate_format_extended import _plate_format_extended
from ._plate_remove_overflows import _plate_remove_overflows

def load_file(path, data_type='SPE', extended=False, **kwargs):
    
    """
    Opens a file dialog window to select a data file. Also runs several
    data adjustment functions depending on the type of data loaded. 
    
    ARGUMENTS:
        path (string): a file path to automatically load a file without
            opening a file dialog window.
        data_type (string): Specifies the type model used to collect the 
            data. Options include 'SPE' (default), 'TEC', and 'PRE'.
        **kwargs: None used, but will accept anyways. 

    RETURNS
        bundle (migration.Bundle): a bundled object containing the raw data
            and the attributes used for storing results. 
        loaded_data (pandas.DataFrame): the dataframe of loaded data in
            case anybody was to access it directly. 
    """
    
    # Generate the new column names
    new_names = []
    for i in range(24):
        new_names.append(f'Column {i + 1}')

    # Caps lock the data type
    data_type = data_type.upper()

    # Create the bundle instance used to store this data
    bundle = Bundle()

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

        elif data_type == 'PRE':  # Pre-prepared bundle data
            
            # Load the data from the excel file
            all_sheets = pd.read_excel(path, sheet_name=None)

            # A couple things get saved to variables for some extra
            # logic and printing later.
            loaded_data = all_sheets['bundle.data.raw'].set_index('<>')
            overflow_meta = all_sheets['bundle.data.overflow_meta']
            num_overflows = overflow_meta.shape[0]

            # Here we'll save to the bundle everything that is not
            # normally included when loading raw data. The 'standard'
            # items (the raw data, overflow meta, etc.) are all saved
            # to the bundle later on. 
            extended = all_sheets['bundle.data.metadata']['extended'][0]
            bundle.data.normalized = all_sheets['bundle.data.normalized'].set_index('<>')
            bundle.data.clean = all_sheets['bundle.data.clean'].set_index('<>')
            bundle.data.average = all_sheets['bundle.data.average']
            bundle.data.peaks_raw = all_sheets['bundle.data.peaks_raw']
            bundle.data.peaks_final = all_sheets['bundle.data.peaks_final']
            bundle.data.ranges_raw = all_sheets['bundle.data.ranges_raw']
            bundle.data.ranges_final = all_sheets['bundle.data.ranges_final']
            bundle.data.radii_nm = all_sheets['bundle.data.radii_nm'].iloc[0].to_dict()

            # Unpack the experimental conditions
            conditions = all_sheets['bundle.data.conditions']
            bundle.data.interval_minutes = conditions['interval_minutes'][0]
            bundle.data.delay_minutes = conditions['delay_minutes'][0]
            bundle.data.load_rate_minutes = conditions['load_rate_minutes'][0]
            bundle.data.temperature_K = conditions['temperature_K'][0]
            bundle.data.method = conditions['method'][0]

        # If the provided data_type doesn't match any known one
        else:
            valid_types = ['TEC', 'SPE', 'PRE']
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
    if extended and data_type != 'PRE':
        loaded_data = _plate_format_extended(input_data=loaded_data, num_reads=num_reads)
    
    # Remove overflow values
    if data_type != 'PRE':
        loaded_data, overflow_meta = _plate_remove_overflows(input_data=loaded_data)
        num_overflows = overflow_meta.shape[0]
    
    # Display warning message about overflow values (if present)
    if num_overflows > 0:
        print(f'ALERT: {num_overflows} overflow value(s) are present in this data set')

    # Save everything into this bundle object
    bundle.data.path = path
    bundle.data.extended = extended
    bundle.data.num_columns = loaded_data.shape[1]
    bundle.data.num_rows = loaded_data.shape[0]
    bundle.data.num_reads = num_reads
    bundle.data.raw = loaded_data
    bundle.data.overflow_meta = overflow_meta

    # Print a confirmation message
    print('Data loading complete')

    # Print some additional information if this was pre-prepared data
    if data_type == 'PRE':
        username = all_sheets['preparation_metadata']['user_prepared'][0]
        dt = datetime.fromtimestamp(all_sheets['preparation_metadata']['datetime_prepared'][0])
        print(f'Prepared by {username} at {str(dt.replace(microsecond=0))}')

    return bundle
