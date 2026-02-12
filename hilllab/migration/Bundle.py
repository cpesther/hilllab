# Christopher Esther, Hill Lab, 8/21/2025
# This class is used by the various migration assay functions so that 
# they can easily pass lots of data around without needing an exorbatant
# number of individual variables and returns. It's basically just a 
# container to keep everything organized. 

import pandas as pd

from ..utilities.print_dict_table import print_dict_table

class Bundle():

    """This is the main container class, it contains separate class
    attributes for the data and the results."""

    def __init__(self):
        self.data = Data()  # raw data and variables
        self.results = Results()  # calculated results values


    def _load_read(self, read_number, type='clean'):

        """
        This is a simple function that pulls one read of data (16 rows 
        at a specific timepoint) from the requested table. The logic is 
        very simple, but since we have to access individual reads so 
        extensively in the codebase, it's helpful to have a dedicated 
        function for consistency and ease-of-use.

        ARGUMENTS:
            read_number (int): the 0-based index of the read that should 
                be pulled. 
            type (string): indicates the table from which the data 
                should be pulled. Possible values include 'raw', 
                'normalized', and 'clean'. 

        RETURNS:
            (pandas.DataFrame): the requested read as a dataframe. 
        """

        # Calculate the indices in the main datafram for the start and end 
        # of the requested read
        read_start_index = int(read_number * 16)
        read_end_index = int(read_start_index + 16)
        
        # Pull and return read from the specified table
        if type == 'raw':
            return self.data.raw[read_start_index:read_end_index]
        
        elif type == 'normalized':
            return self.data.normalized[read_start_index:read_end_index]
        
        else:
            return self.data.clean[read_start_index:read_end_index]


    def __repr__(self):

        # Define the contents dicts with false values first
        keys = ['Normalization', 'Localization', 'Radii', 'Results', 'Calibration', 'Groups']
        contents = {}
        for key in keys:
            contents[key] = False

        # Run through a bunch of checks to see what components are included in this bundle
        if self.data.normalized is not None:
            contents['Normalization'] = True
        if self.data.peaks_raw.shape[0] > 0:
            contents['Localization'] = True
        if self.data.radii_nm is not None:
            contents['Radii'] = True
        if self.results.plate_eta.shape[0] > 0:
            contents['Results'] = True
        if self.results.plate_eta_calib.shape[0] > 0:
            contents['Calibration'] = True
        if len(self.data.groups.keys()) > 0:
            contents['Groups'] = True
            
        # Format this information into a string
        display = f'---- migration.Bundle ----\nFrom: {self.data.path}\n\n'
        for key in contents.keys():
            whitespace = 18 - len(key)
            if contents[key] is True:
                status_value = '■ True'
            else:
                status_value = '□ False'
            display += f"{key}{' '*whitespace}{status_value}\n"

        return display


class Data():

    """
    This class (included as a part of the Bundle container) stores
    all of the raw and cleaned experimental data and relevent parameters. 
    It is generally not written to after the data has been loaded. 
    """

    def __init__(self):

        # Some metadata variables
        self.path = ''
        self.extended = False
        self.num_columns = 0
        self.num_rows = 0
        self.num_reads = 0
        self.overflow_meta = None

        # Here are the dataframes containing the actual experimental data
        self.raw = None  # placeholders until assigned
        self.normalized = None
        self.clean = None
        self.average = None

        # Dataframes containing peak profiling and adjustment data
        self.peaks_raw = pd.DataFrame()
        self.peaks_final = pd.DataFrame()

        # Tables containing Gaussian range locazliation data
        self.ranges_raw = pd.DataFrame()
        self.ranges_final = pd.DataFrame()
        
        # Experimental conditions
        self.radii_nm = None  # in nanometers
        self.interval_minutes = 15  # in minutes
        self.delay_minutes = 0  # in minutes
        self.load_rate_minutes = 1.5  # in minutes
        self.temperature_K = 297  # in K
        self.method = ''

        # Further analysis and visualization
        self.groups = {}


    def show_conditions(self):
        """Prints a summary table of the experimental conditions."""
        
        # Gather experimental conditions
        conditions_dict = {}
        conditions_dict['Extended Mode'] = self.extended
        conditions_dict['# Reads'] = self.num_reads
        conditions_dict['Interval (minutes)'] = self.interval_minutes
        conditions_dict['Delay (minutes)'] = self.delay_minutes
        conditions_dict['Load Rate (minutes)'] = self.load_rate_minutes
        conditions_dict['Temperature (K)'] = self.temperature_K
        conditions_dict['Method'] = self.method

        print_dict_table(conditions_dict, title='Conditions')

    
    def show_radii(self):
        """Prints a summary table of the radii in the bundle."""
        print_dict_table(self.radii_nm, title='Radii')


class Results():

    """
    This class (included as a part of the Bundle container) stores
    all of the results values created by the functions during processing.
    """

    def __init__(self):

        # Raw results
        self.plate_eta = pd.DataFrame()
        self.plate_Dt = pd.DataFrame()
        self.plate_D = pd.DataFrame()
        self.plate_nrmse = pd.DataFrame()
        self.plate_peak = pd.DataFrame()

        # Calibrated results
        self.calib_radii_nm = {}
        self.plate_eta_calib = pd.DataFrame()
        self.plate_D_calib = pd.DataFrame()
