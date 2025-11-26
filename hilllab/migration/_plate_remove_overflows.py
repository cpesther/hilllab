# Christopher Esther, Hill Lab, 8/21/2025
import re
import pandas as pd

def _plate_remove_overflows(input_data):

    """
    Removes 'overflow' values from the provided data by calculating an 
    appropriate numerical value to replace it. This function is called 
    directly after loading a file as a part of load_file.

    ARGUMENTS:
        input_data (pandas.DataFrame): the dataframe containing the 
            raw data that may contain overflows. 

    RETURNS:
        no_overflow_data (pandas.DataFrame): the dataframe with any
            overflow values removed and replaced.
        overflow_meta (pandas.DataFrame): a dataframe containing
            metadata about any overflows that were removed. 
    """

    # Create a new dataframe to store the results
    no_overflow_data = pd.DataFrame(columns=input_data.columns)
    
    # And create a dataframe to store metadata about where any overflow
    # values occur
    overflow_meta = pd.DataFrame(columns=['Column', 'Read', 'Table Row', 
        'Read Row', 'Removed', 'Replacement'])

    # For every column in the provided data
    for column in input_data.columns:
        
        # Pull the column that we'll apply modifications to
        one_column = input_data[column].to_numpy()
        
        # Iterate through each value in the column
        for index, value in enumerate(one_column):
            
            # If the value is alphabetical (i.e. not a number)
            if bool(re.search(r'[a-zA-Z]', str(value))):

                # Pull the next 10 values from the array as potential replacements
                potential_replacements = one_column[index + 1:index + 11]
                chosen_replacement = 0  # reset the chosen_replacement value
                
                # Iterate through the potential replacements to find the
                # first one that is a numeric value (in case more than 
                # one overflow value occurs sequentially)
                for one_replacement in potential_replacements:

                    # If the value is not alphabetical, it't the chosen one
                    if not re.search(r'[a-zA-Z]', str(one_replacement)):
                        chosen_replacement = one_replacement
                        break

                # Log this occurence and populate the overflow meta table
                read_number = index // 16
                index_in_read = index - (read_number * 16)
                overflow_meta_row = [column, read_number, index, index_in_read, value, chosen_replacement]
                overflow_meta.loc[len(overflow_meta)] = overflow_meta_row
                
                # And replace the overflow value with this chosen replacement
                one_column[index] = chosen_replacement
                   
        # Append the column to the new dataframe without overflows
        no_overflow_data[column] = one_column

    # Add and set the index for the cleaned dataframe
    no_overflow_data = no_overflow_data.set_index(input_data.index) 

    return no_overflow_data, overflow_meta
