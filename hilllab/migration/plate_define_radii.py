# Christopher Esther, Hill Lab, 2/9/2026
from ..utilities.print_dict_table import print_dict_table

def plate_define_radii(bundle, radius_nm):

    """
    A backend function for the user to input radius values when 
    processing a plate with multiple different radii.

    ARGUMENTS:
        bundle (migration.Bundle): the bundle object to which these 
            radii values should be saved.
        radius_nm (string or float): a value for the radius or the string
            'multi' to define multiple different radii. 
    
    """

    # Determine the number of columns in the raw data
    num_columns = bundle.data.num_columns
    
    # Entering multi input mode 
    if radius_nm == 'multi':

        # Dict for storing radii values
        input_radii_values = {}

        # Print the header with tooltip information
        print('Tools: \nblank  = Same as previous column\n' \
              's##    = Repeat value until column (s24 repeats current value until column 24)\n' \
              'e      = Finish and exit\n')

        # Iterate over each column in the dataset
        for column in range(1, num_columns + 1):

            # Check if a radii value has already been assigned for this column 
            try:
                input_radii_values[f'Column {int(column)}']
                continue  # continue if one has already been assigned

            # If not, go through the steps to determine one
            except KeyError:
                
                # Ask for the radius input
                one_radius = input(f"Column {column}/{num_columns} radius (nm): ")

                # If a blank field submitted, use previous valuea
                if one_radius == '':
                    one_radius = input_radii_values[f'Column {column - 1}']
                    input_radii_values[f'Column {column}'] = one_radius

                # Process our special radius handling codes
                elif 'e' in one_radius:
                    break  # 'e' is the escape code

                # If copying the previous values to preceeding columns
                elif 's' in one_radius:
                    
                    # Pull the final column of the range and previous radius value
                    previous_radius = input_radii_values[f'Column {column - 1}']
                    final_column = int(one_radius.upper().split('S')[-1])

                    # Repeat it as many times as necessary based on the input
                    for scolumn in range(column, final_column + 1):  # plus 1 for inclusive range
                        input_radii_values[f'Column {scolumn}'] = previous_radius

                # If no special codes were used, just add value as normal
                else:
                    input_radii_values[f'Column {column}'] = one_radius

        # Remove any keys greater than the number of columns (accidentally added)
        remove_keys = []
        for key in input_radii_values.keys():
            if int(key.split('Column ')[1]) > num_columns:
                remove_keys.append(key)
        for key in remove_keys:
            del input_radii_values[key]

        # Display the radii values and ask for confirmation
        print('\n')
        print_dict_table(input_radii_values, title='Radii (nm)')
        confirmation = input('Are these radii values correct? [y]/n ')

        # Handle the response
        if (confirmation == '') or (confirmation.upper() == 'Y'):
            radii_values = input_radii_values
        else:
            print('Trying again...')
            plate_define_radii(bundle=bundle, radius_nm=radius_nm)

    # If a list was provided, load them in one by one
    elif type(radius_nm) is list:
        radii_values = {}
        for column, radius in enumerate(radius_nm):
            radii_values[f'Column {column + 1}'] = radius

    # Otherwise the radius value is probably just one number
    else:
        try:
            radius_value = float(radius_nm)
        except TypeError:
            raise ValueError("Radius value must be a float, list, or 'multi'")
        
        # Repeat this radii value for all columns
        radii_values = {}
        for i in range(1, num_columns):
            radii_values[f'Column {i}'] = radius_value

    return radii_values
