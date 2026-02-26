# Christopher Esther, Hill Lab, 2/23/2026
import tkinter as tk
import numpy as np

from ...utilities.gui.Tooltip import Tooltip
from ...utilities.gui.Popup import Popup
from ...utilities.warning import warn
from ._parameter_window_text import _parameter_window_text

def _parameter_window(parameters='all'):

    """
    Opens GUI window for assigning groups, setting radius values, and 
    indiciating calibration columns. 

    ARGUMENTS:
        parameters (string): controls which fields are shown in the selction
            window, allowing this function to be used for inputting
            either groups, radii, or eta calibration values, or all
            three at once. One of 'all', 'groups', 'radii', or 'calibration'. 
    """

    # Validate the parameters argument and warn the user if it's an 
    # unexpected value
    valid_parameters = ['all', 'groups', 'radii', 'calibration']
    if parameters not in valid_parameters:
        warn(msg=f"'{parameters}' is not a valid parameters value. Defaulting to 'all'.")

    # Some variables to store the data we'll output
    groups = {}
    radii_values = {}
    calibration_columns = {}

    # Create the main window
    root = tk.Tk()

    # Adjust window name and size based on the parameters that this
    # window is being used to display. The columns dictionary is also 
    # being used to manually specify the column indices for certain fields
    # so that everything displays as compactly as possible even when we
    # exclude certain fields. 
    height = 550
    if parameters == 'groups':
        title = '1D Group Assignment'
        width = 600
        n_grid_columns = 6
        columns ={
            'group_name_field': 5,
            }

    elif parameters == 'radii':
        title = '1D Radii Assignment'
        width = 500
        n_grid_columns = 6
        columns ={
            'radius_field': 5,
            }
        
    elif  parameters == 'calibration':
        title = '1D Calibration Assignment'
        width = 500
        n_grid_columns = 6
        columns ={
            'eta_field': 5
            }
        
    else:  # Otherwise we're displaying it all
        title = '1D Parameters Assignment'
        width = 800
        n_grid_columns = 9
        columns ={
            'group_name_field': 5,
            'radius_field': 6,
            'eta_field': 7
            }
        parameters = 'all'
        
    # Set window geometry and title
    root.geometry(f'{width}x{height}')
    root.title(title)

    # Frame for the title and instructions text
    top_frame = tk.Frame(root)
    top_frame.grid(row=0, column=0, columnspan=n_grid_columns + 1, sticky='we', padx=10, pady=10)

    # Add a title
    title_label = tk.Label(top_frame, text=title)
    title_label.config(font=('Helvetica', 16, 'bold'))
    title_label.pack(anchor='w')

    # Add instructions
    wrap_length = width - 20
    inst = _parameter_window_text(parameters=parameters)
    instructions = tk.Label(top_frame, text=inst, justify='left', wraplength=wrap_length)
    instructions.config(font=('Helvetica', 10,))
    instructions.pack(anchor='w')

    # Add the header rows
    group_header = tk.Label(root, text='#')
    group_header.config(font=('Helvetica', 10, 'bold'))
    group_header.grid(column=0, row=2, padx=15, pady=0, sticky='W')

    # Start header
    start_header = tk.Label(root, text='Start')
    start_header.config(font=('Helvetica', 10, 'bold'))
    start_header.grid(column=1, row=2, padx=5, pady=0, sticky='W')
    Tooltip(start_header, 'If including a continuous range of columns, this is the first column of said range.')

    # End header
    end_header = tk.Label(root, text='End')
    end_header.config(font=('Helvetica', 10, 'bold'))
    end_header.grid(column=2, row=2, padx=5, pady=0, sticky='W')
    Tooltip(end_header, 'If including a continuous range of columns, this is the last column of said range.')

    # Columns header
    columns_header = tk.Label(root, text='Columns')
    columns_header.config(font=('Helvetica', 10, 'bold'))
    columns_header.grid(column=4, row=2, padx=5, pady=0, sticky='W')
    Tooltip(columns_header, 'A comma-separated list of column numbers to be included in this group.')

    # Only display the headers requested for the specific parameters
    # Group name header
    if parameters in ['all', 'groups']:
        group_name_header = tk.Label(root, text='Group Name')
        group_name_header.config(font=('Helvetica', 10, 'bold'))
        group_name_header.grid(column=columns['group_name_field'], row=2, padx=5, pady=0, sticky='W')
        Tooltip(group_name_header, 'The name assigned to this group.')

    # Radius header
    if parameters in ['all', 'radii']:
        radius_header = tk.Label(root, text='Radius')
        radius_header.config(font=('Helvetica', 10, 'bold'))
        radius_header.grid(column=columns['radius_field'], row=2, padx=5, pady=0, sticky='W')
        Tooltip(radius_header, 'The radius value of the probe in this group in nanometers.')

    # Calibration header
    if parameters in ['all', 'calibration']:
        eta_header = tk.Label(root, text='Eta')
        eta_header.config(font=('Helvetica', 10, 'bold'))
        eta_header.grid(column=columns['eta_field'], row=2, padx=5, pady=0, sticky='W')
        Tooltip(eta_header, 'If a value is provided, this eta value (in mPa•s) will be used for calibration ' \
            'of the other columns.')

    # Configure grid to have small columns
    for i in range(n_grid_columns):
        root.grid_columnconfigure(i, minsize=10)

    # This dict is used to store references to the widgets so we can pull
    # their values later. 
    input_widgets = []

    # Create each row input
    n_rows = 15
    for i in range(n_rows):

        # The group number
        group_number = tk.Label(root, text=f'{i+1}')
        group_number.config(font=('Helvetica', 12))
        group_number.grid(column=0, row=(i+4), padx=(15, 2), pady=0, sticky='W')

        # The start and end fields
        start_field = tk.Entry(root, width=6)
        start_field.grid(column=1, row=(i+4), padx=5, pady=0, sticky='W')
        end_field = tk.Entry(root, width=6)
        end_field.grid(column=2, row=(i+4), padx=5, pady=0, sticky='W')

        # Subtle 'and' text
        or_text = tk.Label(root, text='and/or')
        or_text.config(font=('Helvetica', 8, 'italic'))
        or_text.grid(column=3, row=(i+4), padx=(3, 3), pady=0, sticky='W')
        
        # Columns entry field
        columns_field = tk.Entry(root, width=22)
        columns_field.grid(column=4, row=(i+4), padx=5, pady=0, sticky='W')

        # Do the same thing as above and only create the fields which 
        # were requested according 

        # Group name field
        if parameters in ['all', 'groups']:
            group_name_field = tk.Entry(root, width=40)
            group_name_field.grid(column=columns['group_name_field'], row=(i+4), 
                                  padx=5, pady=0, sticky='W')
        else:
            group_name_field = None

        # Radius field
        if parameters in ['all', 'radii']:
            radius_field = tk.Entry(root, width=14)
            radius_field.grid(column=columns['radius_field'], row=(i+4), 
                              padx=5, pady=0, sticky='W')
        else:
            radius_field = None

        # Calibration eta field
        if parameters in ['all', 'calibration']:
            calibration_eta_field = tk.Entry(root, width=14)
            calibration_eta_field.grid(column=columns['eta_field'], row=(i+4), 
                                       padx=5, pady=0, sticky='W')
        else:
            calibration_eta_field = None
            
        # Save all the releavnt widgets to the dictionary. Widgets that 
        # aren't created (d/t parameters argument) are saved as None. 
        widgets = {
            'group_number': i + 1,
            'start_field': start_field, 
            'end_field': end_field, 
            'columns_field': columns_field,
            'group_name_field': group_name_field, 
            'radius_field': radius_field,
            'calibration_eta_field': calibration_eta_field
        }

        # Save this dictionary to the main array
        input_widgets.append(widgets)

    # The function that runs when the confirmation button is pressed
    def _confirm():

        """
        Pulls and interprets all the values from the fields, sends warnings
        if needed, and returns nicely formatted values. 
        """
        
        # Iterate over every group input row
        for group in input_widgets:

            # Pull the column data from the group
            start = group['start_field'].get()
            end = group['end_field'].get()
            columns = group['columns_field'].get()
            group_number = group['group_number']

            # If no values were provided in any of these fields, skip.
            if (start == '') and (end == '') and (columns == ''): 
                continue

            # Work with column ranges first
            group_columns = []
            if (start != '') and (end != ''):

                # Convert values to ints
                try:
                    start = int(start)
                    end = int(end)

                # Warn if strange value present
                except ValueError:
                    Popup(f'Invalid start or end value in Group {group_number}', 
                          'error', title='Invalid Column Range').show()
                    return

                range_columns = np.arange(int(start), int(end) + 1)
                group_columns.extend(range_columns)

            # Pull any specifically included column numbers
            if columns != '':
                specific_columns = columns.split(',')

                try:
                    specific_columns = [int(c.strip()) for c in specific_columns]
                except ValueError:  # warn on strange values
                    Popup(f'Invalid columns value in Group {group_number}', 
                          'error', title='Invalid Columns Value').show()
                    return

                # Append these columns to the list of all groups
                group_columns.extend(specific_columns)

            # Once again, we'll now pull only the fields which were
            # created according to the parameters argument. 
            if parameters in ['all', 'groups']:

                # Pull the group name
                group_name = group['group_name_field'].get()

                # Warn user if no group name was provided
                if group_name == '':
                    Popup(f'A name was not provided for Group {group}', 'error',
                          'Group Name Missing')
                    return

                # Add these columns to the group dict
                groups[group_name] = group_columns

            # Work with the radii fields
            if parameters in ['all', 'radii']:

                # Check for a radii value
                radius_nm = group['radius_field'].get()

                # Validate radius value
                try:
                    radius_nm = int(radius_nm)
                except ValueError:
                    Popup(f'Missing or invalid radius value in Group {group_number}', 
                        'error', title='Missing Radius Value').show()
                    return
            
                # Add these columns to the radii_values dictionary
                for c in group_columns:
                    radii_values[f'Column {c}'] = radius_nm 

            # Finally, work with the calibration fields
            if parameters in ['all', 'calibration']:

                # Check if these columns are being used for calibration
                calibration_eta = group['calibration_eta_field'].get()
                if calibration_eta != '':

                    # Save these columns to the calibration_columns dict
                    for c in group_columns:

                        try:  # validate eta value as numerical
                            calibration_eta = float(calibration_eta)
                        except ValueError:
                            Popup(f'Invalid eta value in Group {group_number}', 
                                'error', title='Invalid Eta Value').show()
                            return
                        
                        calibration_columns[c] = calibration_eta

        # Finally, destroy the root window after confirming
        root.destroy()

    # Confirmation button 
    confirmaton_button = tk.Button(root, text='Confirm', width=11, command=_confirm)
    confirmaton_button.grid(column=max(columns.values()), row=19, padx=5, pady=15, sticky='E')

    # Run the application
    root.mainloop()

    return groups, radii_values, calibration_columns


# Run as script
if __name__ == '__main__':

    groups, radii_values, calibration_columns = _parameter_window(parameters='calibration')

    print(f'GROUPS:\n{groups}')
    print(f'RADII:\n{radii_values}')
    print(f'CALIBRATION:\n{calibration_columns}')
