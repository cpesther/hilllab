# Christopher Esther, Hill Lab, 12/4/2025
import pandas as pd
from scipy.io import loadmat
import numpy as np
import uuid
from sklearn.decomposition import PCA
from scipy.signal import savgol_filter

from ..utilities.load_vrpn import load_vrpn

def primary_analysis(path, fps, pixel_width):

    """
    Performs a bunch of calculations on a VRPN file whose results can be 
    used for a variety of different other calculations. 

    Parameters returned for each particle include:
    - particle_id: copied over from the VRPN
    - birth_frame: first tracked frame number
    - death_frame: last tracked frame number
    - birth_seconds: first tracked frame number
    - death_seconds: last tracked frame number

    - lifetime_frames: number of frames for which it is present
    - lifetime_range_frames: death frame minus birth frame
    - lifetime_seconds: number of seconds in its lifetime for which it is present
    - lifetime_range_seconds: number of seconds from birth to death
    - lifetime_fraction_alive: porportion of the lifetime_range in which this particle exists
    - total_fraction_alive: proportion of all frames in which this particle exists
    
    - birth_x: the first x coordinate
    - birth_y: the first y coordinate
    - death_x: the last x coordinate
    - death_y: the last y coordinate

    - mean_x: the average x coordinate
    - mean_y: the average y coordinate
    - median_x: the median x coordinate
    - median_y: the median y coordinate
    - std_x: the standard deviation of the x coordinate
    - std_y: the standard deviation of the y coordinate
    - min_x: the minimum x coordinate
    - min_y: the minimum y coordinate
    - max_x: the minimum x coordinate
    - max_y: the minimum y coordinate
    - range_x: the range of the x coordinate
    - range_y: the range of the y coordinate

    - displacement: distance from birth to death position
    - path_length: distance traveled on its path
    - straightness: the straightness of the path (0 = not straight; 1 = perfectly straight)
        (also known as the confinement ratio)
    - rg: the radius of gyration
    - max_distance: the maximum distance from the first position 

    - mean_heading: the average heading (in degrees) of the particles motion
    - median_heading: the median heading of the particles motion
    - std_heading: the standard deviation of the heading values
    - min_heading: the minimum heading value
    - max_heading: the maximum heading value

    - circular_variance: the circular spread of each subsequent movement.

    - mean_angle: the average directional change at a given frame
        (also know as the DCR, this is the angle between sequential track segments)
    - median_angle: the median directional change at a given frame
    - std_angle: the standard deviation of the angle
    - min_angle: the minimum angle
    - max_angle: the maximum angle

    - mean_speed: the average speed of the particle
    - median_speed: the median speed of the particle
    - std_speed: the standard deviation of the speed of the particle
    - min_speed: the minimum speed
    - max_speed: the maximum speed

    - mean_acceleration: the average acceleration of the particle
    - median_acceleration: the median acceleration of the particle
    - std_acceleration: the standard deviation of the acceleration of the particle
    - min_acceleration: the minimum acceleration
    - max_acceleration: the maximum acceleration

    - linearity: the linearity of the particle's movement
    - bb_area: the area of this particles track's bounding box

    - alignment_deg: the angle of the primary direction of motion in degrees
    - alignment_rad: the angle of the primary direction of motion in radians
    - alignment_strength: the strength of the alignment from 0.5 to 1.0
    
    - path: the path to the VRPN from which this bead originated
    - uuid: a unique identifier assigned to this bead
    
    Additionally, the function calculates and returns certain instantaneous
    values for each particle, including:
    - x: x position
    - y: y position
    - angle_deg: directional change angle at each frame in degrees
    - angle_rad: directional change angle at each frame in radians
    - vx: velocity along the x axis
    - vy: velocity along the y axis
    - speed: the instantanous velocity of each particle at each frame
    - ax: acceleration along the x axis
    - ay: acceleration along the y axis
    - acceleration: the instantanous acceleration of each particle at each frame
    - distance: the distance traveled during this frame
    - total_distance: the cumulative distance traveled by this frame
    - pca: the position data projected onto the primary axis from the PCA
    - path: the path to the VRPN from which this bead originated
    - particle_id: the particle ID in the VRPN
    - uuid: a unique identifier assigned to this bead

    Metadata calculated for the entire video:
    - path: the path to the VRPN
    - n_frames: the number of frames in this video
    - fps: the sampling rate of the video in frames per second
    - n_particles: the number of particles found in this video

    ARGUMENTS:
        path (string): the path to the VRPN file
        fps (int): the frame rate of the video
        pixel_width (float): the width of the pixel in micrometers 

    RETURNS:
        summary (pandas.DataFrame): a dataframe containing the
            summary data for each particle
        positions (dict): a dict of dataframes for the instantaneous
            data for each particle by particle ID
        metadata (dict): a few "metadata" like parameters for the entire
            video. 
    """

    # Load the data and isolate the components
    data = load_vrpn(path)

    # Skip emtpy VRPNs
    if data.shape[0] == 0:
        return None

    # Clean the data
    n_frames = int(max(data['frame']) + 1)
    clean_data = data[~np.isnan(data['x'])]  # remove NaNs
    all_particles = np.unique(data['particle_id']).astype(int)
    frame_duration = 1 / fps

    # Compile some metadata
    metadata = {}
    metadata['path'] = str(path)
    metadata['n_frames'] = n_frames
    metadata['fps'] = fps
    metadata['n_particles'] = len(all_particles)

    # Iterate over each bead and perform calculations
    all_particle_data_dfs = []
    all_instant_data_dfs = []
    for particle_id in all_particles:

        # Generate a UUID to help identify this particle
        uid = str(uuid.uuid4())

        particle_data = {}
        particle_data['particle_id'] = particle_id

        # Get position data for this bead
        one_particle_VRPN = clean_data[clean_data['particle_id'] == particle_id]

        # Start with some of the easy "metadata" calculations
        frame_numbers = one_particle_VRPN['frame']  # the frame number at which this particle exists
        birth_frame = int(min(frame_numbers))
        death_frame = int(max(frame_numbers))
        particle_data['birth_frame'] = birth_frame
        particle_data['death_frame'] = death_frame
        particle_data['birth_seconds'] = birth_frame * frame_duration
        particle_data['death_seconds'] = death_frame * frame_duration

        particle_data['lifetime_frames'] = len(frame_numbers)
        lifetime_range_frames = int(particle_data['death_frame'] - particle_data['birth_frame']) + 1
        particle_data['lifetime_range_frames'] = lifetime_range_frames
        lifetime_seconds = len(frame_numbers) * frame_duration
        particle_data['lifetime_seconds'] = lifetime_seconds
        particle_data['lifetime_range_seconds'] = lifetime_range_frames * frame_duration
        
        particle_data['life_fraction_alive'] = particle_data['lifetime_frames'] / (particle_data['lifetime_range_frames'])
        particle_data['total_fraction_alive'] = particle_data['lifetime_frames'] / n_frames

        # Pull just the coordinate positions
        x = np.array(one_particle_VRPN['x']) * pixel_width  # convert to provided unit of measure
        y = np.array(one_particle_VRPN['y']) * pixel_width

        # Coordinate-related calculations
        mean_x = np.mean(x)
        mean_y = np.mean(y)

        x0, y0 = x[0], y[0]
        particle_data['birth_x'] = x0
        particle_data['birth_y'] = y0
        particle_data['death_x'] = x[-1]
        particle_data['death_y'] = y[-1]
        
        particle_data['mean_x'] = mean_x
        particle_data['mean_y'] = mean_y
        particle_data['median_x'] = np.median(x)
        particle_data['median_y'] = np.median(y)
        particle_data['std_x'] = np.std(x)
        particle_data['std_y'] = np.std(y)
        particle_data['min_x'] = np.min(x)
        particle_data['min_y'] = np.min(y)
        particle_data['max_x'] = np.max(x)
        particle_data['max_y'] = np.max(y)
        particle_data['range_x'] = particle_data['max_x'] - particle_data['min_x']
        particle_data['range_y'] = particle_data['max_y'] - particle_data['min_y']

        # Distance and path-related parameters
        displacement = np.linalg.norm([x[-1] - x[0], y[-1] - y[0]])
        length_segments = np.sqrt(np.diff(x)**2 + np.diff(y)**2)
        path_length = np.sum(length_segments)
        straightness = displacement / path_length if path_length > 0 else 0
        rg = np.sqrt(np.mean((x - mean_x)**2 + (y - mean_y)**2))
        distances_from_origin = np.sqrt((x - x0)**2 + (y - y0)**2)

        particle_data['displacement'] = displacement
        particle_data['path_length'] = path_length
        particle_data['straightness'] = straightness
        particle_data['rg'] = rg
        particle_data['max_distance'] = max(distances_from_origin)
        
        # Step vectors
        dx = np.diff(x)
        dy = np.diff(y)

        # Calculate heading at each point
        headings_rad = np.arctan2(dy, dx)
        headings_deg = np.degrees(headings_rad)
        headings_deg = (headings_deg + 360) % 360
        particle_data['mean_heading'] = np.mean(headings_deg)
        particle_data['median_heading'] = np.median(headings_deg)
        particle_data['std_heading'] = np.std(headings_deg)
        particle_data['min_heading'] = np.min(headings_deg)
        particle_data['max_heading'] = np.max(headings_deg)

        # Calculate circular variance
        resultant = np.sqrt(np.mean(np.cos(headings_rad))**2 + np.mean(np.sin(headings_rad))**2)
        circular_variance = 1 - resultant
        particle_data['circular_variance'] = circular_variance

        # Calculate directional change angles between each subsequent segment
        vectors = np.column_stack((dx, dy))
        norms = np.linalg.norm(vectors, axis=1)  # norms of vectors
        dot_products = np.einsum('ij,ij->i', vectors[:-1], vectors[1:])  # dot products between consecutives
        angles_rad = np.arccos(np.clip(dot_products / (norms[:-1] * norms[1:]), -1.0, 1.0))
        angles_deg = np.degrees(angles_rad)
        particle_data['mean_angle'] = np.mean(angles_deg)
        particle_data['median_angle'] = np.median(angles_deg)
        particle_data['std_angle'] = np.std(angles_deg)
        particle_data['min_angle'] = np.min(angles_deg)
        particle_data['max_angle'] = np.max(angles_deg)

        # Calculate speed at each point
        dt = 1 / fps
        vx = dx / dt
        vy = dy / dt
        speed = np.sqrt(vx**2 + vy**2)
        mean_speed = np.mean(speed)
        particle_data['mean_speed'] = mean_speed
        particle_data['median_speed'] = np.median(speed)
        particle_data['std_speed'] = np.std(speed)
        particle_data['min_speed'] = np.min(speed)
        particle_data['max_speed'] = np.max(speed)
        
        # Calculate acceleration at each point
        ax = np.diff(vx) / dt
        ay = np.diff(vy) / dt
        acceleration = np.sqrt(ax**2 + ay**2)
        particle_data['mean_acceleration'] = np.mean(acceleration)
        particle_data['median_acceleration'] = np.median(acceleration)
        particle_data['std_acceleration'] = np.std(acceleration)
        particle_data['min_acceleration'] = np.min(acceleration)
        particle_data['max_acceleration'] = np.max(acceleration)

        # Calculate linearity of forward progression
        mean_straight_speed = displacement / lifetime_seconds
        linearity = mean_straight_speed / mean_speed
        particle_data['linearity'] = linearity

        # Calculate bounding box area
        x_min, x_max = np.min(x), np.max(x)
        y_min, y_max = np.min(y), np.max(y)
        bb_width = x_max - x_min
        bb_height = y_max - y_min
        bb_area = bb_width * bb_height
        particle_data['bb_area'] = bb_area

        # Calculate the PCA of the coordinate data
        # Format data for PCA and interpolate missing values
        xy_data = one_particle_VRPN[['x', 'y']].interpolate(method='linear')

        # Run PCA
        pca = PCA(n_components=1)
        pca.fit(xy_data)

        # Extract the first principal axis (a 2-element vector) and normalize
        axis = pca.components_[0]
        axis = axis / np.linalg.norm(axis)

        # Project xy data onto the axis from the PCA
        centered = xy_data - xy_data.mean()
        projected = centered.values @ axis

        # Record alignment from the PCA
        alignment_rad = np.arctan2(axis[1], axis[0]) % np.pi
        alignment_deg = np.degrees(alignment_rad)
        alignment_strength = pca.explained_variance_ratio_[0]
        particle_data['alignment_deg'] = alignment_deg 
        particle_data['alignment_rad'] = alignment_rad 
        particle_data['alignment_strength'] = alignment_strength 

        # Also save the path to the particle row for later analysis
        particle_data['path'] = path
        particle_data['uuid'] = uid

        # Determine window length as 10% of signal length
        window_length = max(int(len(projected) * 0.1), 5)  # ensure at least 5 samples

        # Make window length odd
        if window_length % 2 == 0:
            window_length += 1

        # Ensure window length > polyorder
        polyorder = 3
        if window_length <= polyorder:
            window_length = polyorder + 2  # make it bigger than polyorder
            if window_length % 2 == 0:     # and still odd
                window_length += 1

        # Apply Savitzky-Golay filter
        trend = savgol_filter(projected, window_length=window_length, polyorder=polyorder, mode='interp')
        projected_detrend = projected - trend

        # Append the particle data to the list
        all_particle_data_dfs.append(pd.DataFrame([particle_data]))

        # At this point we'll also compile all the instantaneous data calculated
        # for this partcile into a dataframe and then save it to a dict based
        # on that particles ID number.
        instant_data = pd.DataFrame({
            'x': x,
            'y': y,
            'heading_deg': np.append(None, headings_deg),  # append None at end b/c array is n-1 to coords
            'heading_rad': np.append(None, headings_rad),
            'angle_deg': np.append([None, None], angles_deg),
            'angle_rad': np.append([None, None], angles_rad),
            'vx': np.append(None, vx),
            'vy': np.append(None, vy),
            'speed': np.append(None, speed),
            'ax': np.append([None, None], ax),
            'ay': np.append([None, None], ay),
            'acceleration': np.append([None, None], acceleration),
            'distance': np.append(0, length_segments),
            'total_distance': np.append(0, np.cumsum(length_segments)),
            'pca': projected_detrend,
            'path': np.repeat(path, len(x)),
            'particle_id': np.repeat(particle_id, len(x)),
            'uuid': np.repeat(uid, len(x))
        })
        all_instant_data_dfs.append(instant_data)

    # Combine all the dfs into one
    summary = pd.concat(all_particle_data_dfs).reset_index()
    positions = pd.concat(all_instant_data_dfs).reset_index()
    
    return summary, positions, metadata
