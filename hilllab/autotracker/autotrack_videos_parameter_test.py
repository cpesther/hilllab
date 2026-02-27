# Christopher Esther, Hill Lab, 10/06/2025
import os
from pathlib import Path
import cv2
import trackpy as tp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from IPython.display import clear_output

from ._validate_size import _validate_size
from ..utilities.print_dict_table import print_dict_table
from ..utilities.walk_dir import walk_dir
from ..utilities.warning import warn

def autotrack_videos_parameter_test(video_path, n_frames=1, bead_size_pixels=21, 
                                    max_travel_pixels=5, memory=0, invert=False, **kwargs):

    """Allows the user to test autotracking parameters on a small portion
    of a video's frames before running it on larger batches. 

    Args:
        video_path (str): path to the video to use for testing
        n_frames (int, optional): number of frames to use during the test
            track. Defaults to 5. 
        bead_size_pixels (int, optional): Estimated diameter of the 
            particles in pixels. Default is 21.
        max_travel_pixels (int, optional): Maximum number of pixels a particle 
            can travel between frames for TrackPy to consider it to be
            the same particle. Default is 5. 
        memory (int, optional): Memory parameter for TrackPy's linking, 
            specifying how long particles are remembered between frames. 
            Default is 0.
        invert (bool, optional): when false, bright spots on a dark background
            will be tracked. When true, dark spots on a bright background
            will be tracked. 

    Note: 
        This function does not actually use any kwargs, but it is 
        designed to accept them so that this function can accept all the 
        same arguments as the actual autotrack_videos function, which 
        just makes documentation and usage a lot easier. 
    """

    # Validate bead size argument
    bead_size_pixels = _validate_size(bead_size_pixels=bead_size_pixels)

    # First we'll run some logic to get the exact path to the video we're testing
    if os.path.isfile(video_path):              # if it is a file

        # Make sure it's a video file
        if Path(video_path).suffix.replace('.', '') not in ['avi', 'mp4']:
            raise OSError('The path provided is not a .avi or .mp4 file')
        else:
            track_path = video_path             # we'll track it
    else:                                       # if the path is a folder
        
        # List all video files
        all_files = walk_dir(video_path, extension=['avi', 'mp4'])

        # Verify that some were found
        if len(all_files) == 0:
            raise OSError(f'No video files found in {video_path}')
        
        # Test the first file
        track_path = all_files[0]
        
    print(f'Testing video {track_path}')

    # Create the grayscale conversion function and wrap into PIMS
    cap = cv2.VideoCapture(track_path)
    frames = []
    for _ in range(n_frames):
        ret, frame = cap.read()
        if not ret:
            break
        # Take green channel for single-channel grayscale
        gray_frame = frame[:, :, 1]  
        frames.append(gray_frame)
    cap.release()
    print('Video loaded')

    # Calculate minmass and perform location on first frame
    minmass_value = 750 * (bead_size_pixels / 21) ** 3
    print('Performing tracking...')
    f = tp.batch(frames, bead_size_pixels, minmass=minmass_value, invert=invert)
    print('Tracking complete')

    # Verify that some beads were found
    if len(f) == 0:
        raise RuntimeError('No beads found in this file')

    # Perform linking
    try:
        particle_positions = tp.link(f, max_travel_pixels, memory=memory)
    except Exception:
        warn(msg='Unable to link beads')
    
    # Clear the display
    try:
        clear_output(wait=True)  # clear all print outputs
    except Exception:
        pass

    # Generate the annotated image
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    axes[0].imshow(frames[0], cmap='gray')
    axes[1].imshow(frames[0], cmap='gray')

    # Define and add the circles around the particles
    radius = int(len(frames[0][0]) * 0.01)  # 1% of width
    offset = radius * 1.2
    frame0_positions = particle_positions[particle_positions['frame'] == 0]
    for row in frame0_positions.iterrows():
        x = row[1].x
        y = row[1].y
        circle = patches.Circle((x, y), radius=radius, edgecolor='red', facecolor='none', linewidth=1)
        axes[0].text(x + offset, y - offset, f'{row[0]}', c='red', fontsize=6)
        axes[0].add_patch(circle)

    # Plot the tracking image, if able
    if n_frames > 1:
        for particle in np.unique(particle_positions['particle']):

            # Plot the path of the particle
            one_particle_data = particle_positions[particle_positions['particle'] == particle]
            axes[1].plot(one_particle_data['x'], one_particle_data['y'], c='#00FF00')
    else:
        # Add some prompt text
        axes[1].text(len(gray_frame[0]) / 2, len(gray_frame) / 2, 'Set n_frames > 1 to calculate test path trace', 
                     c='#00FF00', fontsize=10, ha='center', va='center')

    # Gather and calculate some additional information
    info = {
        'Total beads found (f1)': frame0_positions.shape[0],
        'Average mass': round(np.mean(particle_positions['mass']), 3),
        'Average size': round(np.mean(particle_positions['size']), 3),
        'Average signal': round(np.mean(particle_positions['signal']), 3)
    }

    # Pretty print that information as a table
    print_dict_table(dict=info, title='TRACK INFORMATION')

    axes[0].set_title(f'{track_path[-120:]}\nParticle Identification: {frame0_positions.shape[0] + 1} total beads found', fontsize=10)
    axes[1].set_title(f'{track_path[-120:]}\nPath Trace: {n_frames} frames', fontsize=10)

    plt.show()
    return
