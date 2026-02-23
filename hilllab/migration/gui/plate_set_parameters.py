# Christopher Esther, Hill Lab, 2/23/2026
import tkinter as tk
import numpy as np

from ...utilities.gui.Tooltip import Tooltip
from ...utilities.gui.Popup import Popup

def plate_set_parameters():

    """
    Opens GUI window for assigning groups, setting radius values, and 
    indiciating calibration columns. 

    ARGUMENTS:
        bundle (migration.Bundle): the bundles for which the parameters
            should be set. 
    
    """

    # Some variables to store the data we'll output
    groups = {}
    radii_values = {}
    calibration_columns = {}

    # Create the main window
    root = tk.Tk()
    root.title('1D Group Assignment')
    root.geometry('800x550')  # width x height

    # Frame for the title and instructions text
    top_frame = tk.Frame(root)
    top_frame.grid(row=0, column=0, columnspan=9, sticky='we', padx=10, pady=10)

    # Add a title
    title = tk.Label(top_frame, text='1D Group Assignment')
    title.config(font=('Helvetica', 16, 'bold'))
    title.pack(anchor='w')

    # Add instructions
    inst = 'Create groups of capillaries by inputting a name and assigning slot numbers. Groups are used ' \
        'when combining multiple data sets, performing statistical analysis, and generating reports. ' \
        'You can create up to 15 unique groups. Hover over each header for tooltips.'
    instructions = tk.Label(top_frame, text=inst, justify='left', wraplength=700)
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

    # Group name header
    group_name_header = tk.Label(root, text='Group Name')
    group_name_header.config(font=('Helvetica', 10, 'bold'))
    group_name_header.grid(column=5, row=2, padx=5, pady=0, sticky='W')
    Tooltip(group_name_header, 'The name assigned to this group.')

    # Radius header
    radius_header = tk.Label(root, text='Radius')
    radius_header.config(font=('Helvetica', 10, 'bold'))
    radius_header.grid(column=6, row=2, padx=5, pady=0, sticky='W')
    Tooltip(radius_header, 'The radius value of the probe in this group in nanometers.')

    # Calibration header
    eta_header = tk.Label(root, text='Eta')
    eta_header.config(font=('Helvetica', 10, 'bold'))
    eta_header.grid(column=7, row=2, padx=5, pady=0, sticky='W')
    Tooltip(eta_header, 'If a value is provided, this eta value (in mPa•s) will be used for calibration ' \
        'of the other columns.')

    # Configure grid to have small columns
    for i in range(7):
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
        
        # Column entry field
        columns_field = tk.Entry(root, width=22)
        columns_field.grid(column=4, row=(i+4), padx=5, pady=0, sticky='W')

        # Group name field
        group_name_field = tk.Entry(root, width=40)
        group_name_field.grid(column=5, row=(i+4), padx=5, pady=0, sticky='W')
        
        # Radius field
        radius_field = tk.Entry(root, width=14)
        radius_field.grid(column=6, row=(i+4), padx=5, pady=0, sticky='W')

        # Eta field
        calibration_eta_field = tk.Entry(root, width=14)
        calibration_eta_field.grid(column=7, row=(i+4), padx=5, pady=0, sticky='W')
        
        # Save all the releavnt widgets to the dictionary
        widgets = {
            'group_number': i+1,
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

            # Pull the group name
            group_name = group['group_name_field'].get()
            group_number = group['group_number']

            # Skip this group if a group name was not provided
            if group_name == '':
                continue

            # Pull the column data from the group. Specific columns values
            # always take precedence over range values. 
            start = group['start_field'].get()
            end = group['end_field'].get()
            columns = group['columns_field'].get()
            
            # Work with column ranges first
            group_columns = []
            if (start != '') and (end != ''):

                # Convert values to ints
                try:
                    start = int(start)
                    end = int(end)

                except ValueError:
                    Popup(f'Invalid start or end value in Group {group_number}', 
                        'error', title='Invalid Column Range').show()
                    return

                range_columns = np.arange(int(start), int(end) + 1)
                group_columns.extend(range_columns)

            # Pull any specificly included column numbers
            if columns != '':
                specific_columns = columns.split(',')
                specific_columns = [int(c.strip()) for c in specific_columns]
                group_columns.extend(specific_columns)

            # Add these columns to the group dict
            groups[group_name] = group_columns

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

            # Check if these columns are being used for calibration
            calibration_eta = group['calibration_eta_field'].get()
            if calibration_eta != '':

                # Save these columns to the calibration_columns dict
                for c in group_columns:
                    calibration_columns[c] = calibration_eta

        # Finally, destroy the root window after confirming
        root.destroy()

    # Confirmation button 
    confirmaton_button = tk.Button(root, text='Confirm', width=11, command=_confirm)
    confirmaton_button.grid(column=7, row=19, padx=5, pady=15, sticky='W')

    # Run the application
    root.mainloop()

    return groups, radii_values, calibration_columns
