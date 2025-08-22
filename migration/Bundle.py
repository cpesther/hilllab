# Christopher Esther, Hill Lab, 8/21/2025

# This class is used by the various migration assay functions so that 
# they can easily pass lots of data around without needing an exorbatant
# number of individual variables and returns. It's basically just a 
# container to keep everything organized. 

import pandas as pd


class Bundle():

    """This is the main container class, it contains separate class
    attributes for the data and the results."""

    def __init__(self):
        self.data = Data()  # raw data and variables
        self.results = Results()  # calculated results values


    def _load_read(self, read_number, type):

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

        # Here are the dataframes containing the actual experimental data
        self.raw = 'No raw data available'  # placeholder values until assigned
        self.normalized = 'No normalized data available'
        self.clean = 'No clean data available'
        self.average = 'No average data available'

        # Dataframes containing peak profiling and adjustment data
        self.ppd_peaks_raw = pd.DataFrame()
        self.ppd_peaks_final = pd.DataFrame()

        # Tables containing Gaussian range locazliation data
        self.ppd_gaussian_ranges_raw = pd.DataFrame()
        self.ppd_gaussian_ranges_final = pd.DataFrame()

        # The overflow logging table
        self.overflow_meta = 'No overflow metadata available'
        
        # Experimental conditions
        self.radii = 'No radii values available'
        self.interval = 15
        self.delay = 0
        self.load_rate = 1.5
        self.temperature = 297
        self.drift = 0
        self.method = ''


class Results():

    """
    This class (included as a part of the Bundle container) stores
    all of the results values created by the functions during processing.
    """

    def __init__(self):

        # Raw results
        self.plate_viscosity = None
        self.plate_Dt = None
        self.plate_D = None
        self.plate_nrmse = None
        self.plate_peak = None

        # Summary/pretty print tables
        self.plate_summary_eta = None
        self.plate_summary_D = None
        self.plate_summary_analysis = None
