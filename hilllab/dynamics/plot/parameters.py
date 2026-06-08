# Christopher Esther, Hill Lab, 5/11/2026

# Holds all of the paramters captured during the dynamics pipeline as
# well as their display name and units used for plotting. 

PARAMETERS = {
    'birth_frame': {
        'display_name': 'Birth Frame',
        'units': 'frame'
    },
    'death_frame': {
        'display_name': 'Death Frame',
        'units': 'frame'
    },
    'birth_seconds': {
        'display_name': 'Birth Time',
        'units': 's'
    },
    'death_seconds': {
        'display_name': 'Death Time',
        'units': 's'
    },
    'lifetime_frames': {
        'display_name': 'Lifetime (Frames)',
        'units': 'frame'
    },
    'lifetime_range_frames': {
        'display_name': 'Lifetime Range (Frames)',
        'units': 'frame'
    },
    'lifetime_seconds': {
        'display_name': 'Lifetime',
        'units': 's'
    },
    'lifetime_range_seconds': {
        'display_name': 'Lifetime Range',
        'units': 's'
    },
    'life_fraction_alive': {
        'display_name': r'% of Lifetime Tracked',
        'units': r"% of frames"
    },
    'total_fraction_alive': {
        'display_name': r'% of Video Tracked',
        'units': r"% of frames"
    },
    'birth_x': {
        'display_name': 'Birth X Position',
        'units': "µm"
    },
    'birth_y': {
        'display_name': 'Birth Y Position',
        'units': "µm"
    },
    'death_x': {
        'display_name': 'Death X Position',
        'units': "µm"
    },
    'death_y': {
        'display_name': 'Death Y Position',
        'units': "µm"
    },
    'mean_x': {
        'display_name': 'Mean X Position',
        'units': "µm"
    },
    'mean_y': {
        'display_name': 'Mean Y Position',
        'units': "µm"
    },
    'median_x': {
        'display_name': 'Median X Position',
        'units': "µm"
    },
    'median_y': {
        'display_name': 'Median Y Position',
        'units': "µm"
    },
    'std_x': {
        'display_name': 'X Position Standard Deviation',
        'units': "µm"
    },
    'std_y': {
        'display_name': 'Y Position Standard Deviation',
        'units': "µm"
    },
    'min_x': {
        'display_name': 'Minimum X Position',
        'units': "µm"
    },
    'min_y': {
        'display_name': 'Minimum Y Position',
        'units': "µm"
    },
    'max_x': {
        'display_name': 'Maximum X Position',
        'units': "µm"
    },
    'max_y': {
        'display_name': 'Maximum Y Position',
        'units': "µm"
    },
    'range_x': {
        'display_name': 'X Range',
        'units': "µm"
    },
    'range_y': {
        'display_name': 'Y Range',
        'units': "µm"
    },
    'displacement': {
        'display_name': 'Displacement',
        'units': "µm"
    },
    'path_length': {
        'display_name': 'Path Length',
        'units': "µm"
    },
    'straightness': {
        'display_name': 'Straightness',
        'units': None
    },
    'rg': {
        'display_name': 'Radius of Gyration',
        'units': "µm"
    },
    'max_distance': {
        'display_name': 'Max Distance',
        'units': "µm"
    },
    'mean_heading': {
        'display_name': 'Mean Heading',
        'units': 'degrees'
    },
    'median_heading': {
        'display_name': 'Median Heading',
        'units': 'degrees'
    },
    'std_heading': {
        'display_name': 'Heading Standard Deviation',
        'units': 'degrees'
    },
    'min_heading': {
        'display_name': 'Minimum Heading',
        'units': 'degrees'
    },
    'max_heading': {
        'display_name': 'Maximum Heading',
        'units': 'degrees'
    },
    'circular_variance': {
        'display_name': 'Circular Variance',
        'units': None
    },
    'mean_angle': {
        'display_name': 'Mean Angle',
        'units': 'degrees'
    },
    'median_angle': {
        'display_name': 'Median Angle',
        'units': 'degrees'
    },
    'std_angle': {
        'display_name': 'Angle Standard Deviation',
        'units': 'degrees'
    },
    'min_angle': {
        'display_name': 'Minimum Angle',
        'units': 'degrees'
    },
    'max_angle': {
        'display_name': 'Maximum Angle',
        'units': 'degrees'
    },
    'mean_speed': {
        'display_name': 'Mean Speed',
        'units': "µm/s"
    },
    'median_speed': {
        'display_name': 'Median Speed',
        'units': "µm/s"
    },
    'std_speed': {
        'display_name': 'Speed Standard Deviation',
        'units': "µm/s"
    },
    'min_speed': {
        'display_name': 'Minimum Speed',
        'units': "µm/s"
    },
    'max_speed': {
        'display_name': 'Maximum Speed',
        'units': "µm/s"
    },
    'mean_acceleration': {
        'display_name': 'Mean Acceleration',
        'units': "µm/s²"
    },
    'median_acceleration': {
        'display_name': 'Median Acceleration',
        'units': "µm/s²"
    },
    'std_acceleration': {
        'display_name': 'Acceleration Standard Deviation',
        'units': "µm/s²"
    },
    'min_acceleration': {
        'display_name': 'Minimum Acceleration',
        'units': "µm/s²"
    },
    'max_acceleration': {
        'display_name': 'Maximum Acceleration',
        'units': "µm/s²"
    },
    'linearity': {
        'display_name': 'Linearity',
        'units': None
    },
    'bb_area': {
        'display_name': 'Bounding Box Area',
        'units': 'pixels²'
    },
    'alignment_deg': {
        'display_name': 'Alignment',
        'units': 'degrees'
    },
    'alignment_rad': {
        'display_name': 'Alignment',
        'units': 'radians'
    },
    'alignment_strength': {
        'display_name': 'Alignment Strength',
        'units': None
    },
    'path': {
        'display_name': 'Path',
        'units': None
    },
    'uuid': {
        'display_name': 'UUID',
        'units': None
    },
    'identifier': {
        'display_name': 'Identifier',
        'units': None
    },
    'classification': {
        'display_name': 'Classification',
        'units': None
    },
    'stuck_classification_weight': {
        'display_name': 'Stuck Classification Weight',
        'units': None
    },
    'oscillating_classification_weight': {
        'display_name': 'Oscillating Classification Weight',
        'units': None
    },
    'transiting_classification_weight': {
        'display_name': 'Transiting Classification Weight',
        'units': None
    },
    'group': {
        'display_name': 'Group',
        'units': None
    }
}
