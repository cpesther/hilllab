# Christopher Esther, Hill Lab, 11/20/2025
import numpy as np

def _calculate_force_distance(data, viscosity, origin, diameter):
    """
    Computes log(force) vs log(distance) relationships for each unique voltage.
    Tracks particle motion between the first and last frame for each voltage,
    computes velocity and Stokes drag, and fits a log-log line.

    PARAMETERS:
        data: DataFrame with columns ['t', 'x', 'y', 'PID', 'voltages']
        viscosity: fluid viscosity (Pa*s)
        origin: tuple (x0, y0) for magnetic field origin
        diameter: particle diameter (meters)

    RETURNS:
        List of tuples (voltage, m, c) where:
            log(force) = m*log(distance) + c
    """

    coeffs_at_voltages = []

    # Iterate through each voltage applied in the experiment
    for voltage in np.sort(data['voltage'].unique()):

        # Collect fresh lists for this voltage only
        distances = []
        forces = []

        # First and last frames for this voltage
        subset = data[data['voltage'] == voltage]

        if subset.empty:
            print(f"Skipping voltage {voltage} because it has no data")
            continue

        init_time = subset.iloc[0]['frame']
        final_time = subset.iloc[-1]['frame']

        # Frame subsets
        data_init = subset[subset['frame'] == init_time]
        data_final = subset[subset['frame'] == final_time]

        # Loop across all particle IDs present at the initial frame
        for particle_id in np.sort(data_init['particle']):
            if particle_id not in data_final['particle'].values:
                continue  # particle disappears before final frame

            # Extract coordinates (x1, y1) and (x2, y2)
            row_init = data_init[data_init['particle'] == particle_id].iloc[0]
            row_final = data_final[data_final['particle'] == particle_id].iloc[0]

            x1, y1 = row_init['x'], row_init['y']
            x2, y2 = row_final['x'], row_final['y']

            # Compute velocity magnitude
            dt = final_time - init_time
            if dt == 0:
                continue  # avoid division by zero

            velocity = np.sqrt((x2 - x1)**2 + (y2 - y1)**2) / dt

            # Compute Stokes drag (force applied equals drag under steady motion)
            drag_force = 3 * np.pi * viscosity * diameter * velocity

            # Compute average particle position relative to origin
            x_avg = (x1 + x2) / 2
            y_avg = (y1 + y2) / 2

            dx = origin[0] - x_avg
            dy = origin[1] - y_avg

            distance = np.sqrt(dx*dx + dy*dy)

            # Store for log-log regression
            distances.append(distance)
            forces.append(drag_force)

        # Must have at least two data points for a fit
        if len(distances) < 2:
            print(f"Skipping voltage {voltage}: insufficient data for log-log fit.")
            continue

        # Fit log(force) = m * log(distance) + c
        logs_d = np.log(distances)
        logs_f = np.log(forces)

        m, c = np.polyfit(logs_d, logs_f, 1)

        coeffs_at_voltages.append((voltage, m, c))

    return coeffs_at_voltages
