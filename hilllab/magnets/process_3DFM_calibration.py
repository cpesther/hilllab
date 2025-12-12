# Christopher Esther, Hill Lab, 11/20/2025
import cv2
from pathlib import Path
import numpy as np
import trackpy as tp
import os
import pandas as pd
from scipy.signal import find_peaks
from scipy.io import loadmat
import pickle

# These neighboring imports are desinged to work both within the hilllab
# module and when the function is being run as a loose script.
try:
    from ._get_pole_tip import _get_pole_tip
except ImportError:
    from _get_pole_tip import _get_pole_tip

try:
    from ..magnets._calculate_origin_from_lines import _calculate_origin_from_lines
except ImportError:
    from magnets._calculate_origin_from_lines import _calculate_origin_from_lines

try:
    from ..magnets._remove_wide_angles import _remove_wide_angles
except ImportError:
    from magnets._remove_wide_angles import _remove_wide_angles

try:
    from ..magnets._calculate_force_distance import _calculate_force_distance
except ImportError:
    from magnets._calculate_force_distance import _calculate_force_distance

try:
    from ..utilities.print_progress_bar import print_progress_bar
    show_progress = True
except ImportError:
    from utilities.print_progress_bar import print_progress_bar
    show_progress = True
else:
    show_progress = False


def process_3DFM_calibration(video_path, voltage_path,
                             bead_size_pixels=23, trajectory_fraction=0.05, max_travel_pixels=5, 
                             memory=0, invert=True, performance_mode='safe', manual_lag=-10, 
                             displacement_threshold=50, angle_threshold=30):

    """
    Performs particle tracking, voltage synchronization, and force-distance
    calculations on a calibration video from the 3DFM.

    ARGUMENTS:
        video_path (str): the path to the video to be processed.
        voltage_path (str): the path to the matlab file containing
            the voltages and durations.
        bead_size_pixels (int, optional): Estimated diameter of the 
            particles in pixels. Default is 23.
        trajectory_fraction (float, optional): Minimum fraction of frames a 
            particle must appear in to be retained after filtering. 
            Default is 1.0.
        max_travel_pixels (int, optional): Maximum number of pixels a particle 
            can travel between frames for TrackPy to consider it to be
            the same particle. Default is 5. 
        memory (int, optional): Memory parameter for TrackPy's linking, 
            specifying how long particles are remembered between frames. 
            Default is 0.
        invert (bool, optional): when false, bright spots on a dark background
            will be tracked. When true, dark spots on a bright background
            will be tracked. 
        performance_mode (string, 'safe', 'slow', or 'fast'): Controls 
            how many processes are used by TrackPy to allow this task to
            be run safely in the background or sped up on demand. 
        manual_lag (int, optional): the number of frames the voltage signal
            should be shifted in addition to that calculated by the
            correlation. 
        displacement_threshold (int, optional): the minimum displacement a 
            particle must exhibit to be considered "in-motion" and therefore
            be included in the force calculations. 
        angle_threshold (int, optional): the maximum angle at which a particles
            vector may intersect with the pole tip/origin axis before
            being excluded as an "off angle" particle. 

    OUTPUTS:
        Outputs all trajectories, the filtered "narrow" trajectories, 
        and the coefficients at each voltage to an Excel file with 
        the name of the video. 
    """

    # Start by loading the video
    print('Loading video...')
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f'Cannot open video {video_path}')
    
    try:
        raw_voltage_file = loadmat(voltage_path)  # open the matlab file

        # Pull all the needed information
        raw_voltages = raw_voltage_file['voltages'][0]
        raw_times = raw_voltage_file['pulse_widths'][0]
        n_segments = raw_voltage_file['NRepeats'][0][0]
        viscosity = raw_voltage_file['calibrator_viscosity'][0][0]
        diameter = raw_voltage_file['bead_radius'][0][0] * 2 * 1e-6
        fps = raw_voltage_file['fps'][0][0]

        # Assemble the voltages table
        voltage_table = pd.DataFrame({'voltage': raw_voltages, 'time': raw_times})
    
    except Exception as e:
        print(e)
        raise ValueError('ERROR: Voltages file must be either .xlsx or .csv')
    
    # Calculate some details
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Reset cap read, just to be safe
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Preallocate array for grayscale frames
    grayscale_frames = np.zeros((num_frames, frame_height, frame_width), dtype=np.uint8)

    # Iterate over each frame and convert to grayscale
    for i in range(num_frames):

        # Show a progress bar, if possible
        if show_progress:
            print_progress_bar(total=num_frames, progress=i+1, title='Converting to grayscale')
        ret, frame = cap.read()
        if not ret:
            break
        # Convert frame to grayscale using OpenCV
        grayscale_frames[i] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cap.release()  # release the video so it can be accessed by other programs
    print('\n')    # reset from the progress bar

    # Ask the user for the location of the pole tip
    pole_tip = _get_pole_tip(frame)

    # Determine how many processes to allow TrackPy to use
    if performance_mode == 'slow':
        num_processes = os.cpu_count() / 2
    elif performance_mode == 'fast':
        num_processes = os.cpu_count()
    else:  # 'safe' mode, or any other value
        num_processes = os.cpu_count() - 2

    # Perform tracking
    minmass_value = 3000 * (bead_size_pixels / 23) ** 3
    particle_positions = tp.batch(grayscale_frames, bead_size_pixels, minmass=minmass_value, 
                processes=int(num_processes), invert=invert)
    
    # Link positions
    raw_linked_positions = tp.link(particle_positions, max_travel_pixels, memory=memory)

    # Remove any particles that don't last for enough frames
    print('Removing short tracks...')
    frame_threshold = len(grayscale_frames) * trajectory_fraction
    linked_positions = tp.filter_stubs(raw_linked_positions, threshold=frame_threshold)

    # We're only interested (especially for the purpose of signal matching) 
    # in the particles that move, so we'll calculate the net displacement
    # of each particle so we can filter out the stationary ones.
    print('Calculating particle stats...')
    displacements = linked_positions.groupby('particle')[['x','y']].apply(
        lambda df: ((df['x'].max() - df['x'].min())**2 + (df['y'].max() - df['y'].min())**2)**0.5
    )
    lifetimes = linked_positions.groupby('particle')['frame'].count()

    # Combine into df
    particle_stats = pd.DataFrame({'displacement': displacements, 
                                'lifetime': lifetimes})

    # Filter out the particles that meet the criteria for movement
    filtered_particle_stats = particle_stats[(particle_stats['displacement'] > displacement_threshold)]

    # Now apply this filter to the linked positions table
    filtered_linked_positions = linked_positions[linked_positions['particle'].isin(filtered_particle_stats.index)]
    filtered_linked_positions = filtered_linked_positions.reset_index(drop=True)  # drop index

    # Sort by particle and frame just in case
    filtered_linked_positions = filtered_linked_positions.sort_values(['particle', 'frame'])

    # Print message about how many particles are considerd to be moving
    num_moving = len(np.unique(filtered_linked_positions['particle']))
    print(f'{num_moving} moving particle(s) detected')

    # Compute frame-to-frame displacements
    filtered_linked_positions['dx'] = filtered_linked_positions.groupby('particle')['x'].diff()
    filtered_linked_positions['dy'] = filtered_linked_positions.groupby('particle')['y'].diff()

    # Compute velocity magnitude (pixels per frame)
    filtered_linked_positions['velocity'] = np.sqrt(
        filtered_linked_positions['dx']**2 + filtered_linked_positions['dy']**2
    )

    # Calculate average velocity magnitude of all moving particles in each frame
    avg_frame_vel = filtered_linked_positions.groupby('frame')['velocity'].mean()
    avg_frame_vel = avg_frame_vel[np.isfinite(avg_frame_vel)]  # remove NaNs

    # Smooth the velocity curve
    window = int(num_frames * 0.02)
    n_avg_frame_vel = avg_frame_vel / max(avg_frame_vel)
    velocity = np.convolve(n_avg_frame_vel, np.ones(window) / window, mode='same')

    # Build the actual signal from the values with frames as the time unit
    voltage_segment = []
    for row in voltage_table.iterrows():

        one_voltage = row[1].iloc[0]
        n_frames = row[1].iloc[1] * fps  # calculate the number of frames this voltage must last
        voltage_segment.extend(np.repeat(one_voltage, round(n_frames)))

    # And repeat the entire signal chunk according to the n segments
    voltage = np.tile(voltage_segment, n_segments)

    # Generate a "scrunched" voltage signal that can be used for better correlation
    # Find the basline minimum velocity values 
    min_indices, _ = find_peaks(-velocity)  # find peaks in the inverted signal
    min_values = velocity[min_indices]  # values of the minima
    min_velocity = np.median(min_values)

    # And the maximum velocity values 
    max_indices, _ = find_peaks(velocity, width=fps)
    max_values = velocity[max_indices]  # values of the maxima
    max_velocity = np.median(max_values)

    # Min-max normalize the voltage signal
    a, b = min_velocity, max_velocity  # desired normalization range (a is min, b is max)
    n_voltage = a + (voltage - voltage.min()) * (b - a) / (voltage.max() - voltage.min())

    # temp
    with open('vals.pkl', 'wb') as f:
        pickle.dump([velocity, n_voltage], f)


    # Perform the correlation
    corr = np.correlate(velocity, n_voltage, mode='full')  # full correlation
    lags = np.arange(-len(n_voltage) + 1, len(velocity))  # index of shifts

    # Find the lag where correlation is maximum
    lag_index = np.argmax(corr)
    time_offset = lags[lag_index]
    print(f'Voltage alignment lag calculated as {time_offset} frames.')

    # Combine automatic cross-correlation lag and manual lag
    total_lag = time_offset + manual_lag  # positive = shift right (pad start), negative = shift left (pad end)

    if total_lag > 0:
        # pad start
        voltage_shifted = np.pad(voltage, (total_lag, 0), mode='constant')
    elif total_lag < 0:
        # pad end
        voltage_shifted = np.pad(voltage, (0, -total_lag), mode='constant')
    else:
        voltage_shifted = voltage

    # Ensure voltage matches velocity length exactly
    if len(voltage_shifted) < len(velocity):
        voltage_shifted = np.pad(voltage_shifted, (0, len(velocity) - len(voltage_shifted)), mode='constant')
    else:
        voltage_shifted = voltage_shifted[:len(velocity)]

    # Create a mapping from frame number to voltage
    final_positions = filtered_linked_positions.copy()
    frame_to_voltage = {frame: voltage_shifted[frame] for frame in range(len(voltage_shifted))}

    # Assign voltage using map
    final_positions['voltage'] = final_positions['frame'].map(frame_to_voltage)

    # Now that out voltage signal is appropriately incorporated into the 
    # tracking data, we can shift gears and start working with the actual
    # tracking data. 
    # Calculate the line of each particle's motion
    lines = []

    # Iterate over each particle
    for particle_id in np.unique(final_positions['particle']):
        
        # Pull this particle's data
        particle_data = final_positions[final_positions['particle'] == particle_id]

        # Skip particles with too few points
        if len(particle_data) < 4:
            print(f"Skipping particle {particle_id}: not enough points")
            continue

        # Calculate indices at 25% and 75% along the trajectory
        idx1 = int(round(0.25 * (len(particle_data) - 1)))
        idx2 = int(round(0.75 * (len(particle_data) - 1)))

        # Extract x and y coordinates (assuming columns 1=x, 0=y)
        x1, y1 = particle_data.iloc[idx1, [1, 0]]
        x2, y2 = particle_data.iloc[idx2, [1, 0]]

        # Store as a vector segment
        lines.append(((x1, y1), (x2, y2)))

    # Use the intersection of these vectors to find the origin of the magnetic field
    origin = _calculate_origin_from_lines(lines)

    # Remove particles moving at angles >n° from the pole tip/origin axis
    narrow_positions = _remove_wide_angles(df=final_positions, origin=origin, 
                                           pole_tip=pole_tip, angle_threshold=angle_threshold)
    print(f"{len(final_positions['particle'].unique()) - len(narrow_positions['particle'].unique())} wide-angle trajectories removed.")

    # Calculate the force vs. distance relationship
    coeffs_at_voltages = _calculate_force_distance(narrow_positions, viscosity, origin, diameter)

    # Package everything up and export to an Excel file
    coeffs_df = pd.DataFrame(coeffs_at_voltages)
    coeffs_df.columns = ['voltage', 'm', 'c']

    output_name = f'{Path(video_path).stem}.xlsx'
    output_path = os.path.join(Path(video_path).parent, output_name)

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        final_positions.to_excel(writer, sheet_name='All Trajectories', index=False)
        narrow_positions.to_excel(writer, sheet_name='Filtered Trajectories', index=False)
        coeffs_df.to_excel(writer, sheet_name='Coefficients', index=False)

    print(f'Results exported as {output_name}')
