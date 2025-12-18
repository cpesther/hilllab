# Christopher Esther, Hill Lab, 10/13/2025
import os
from pathlib import Path
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time
from scipy.io import savemat
import subprocess

def calculate_CBF_FFCA_cs(video_path, sampling_rate=60, power_threshold=5, 
                       skip_existing=True, plot=False):

    """
    Calculates the ciliary beat frequency (CBF) from a brightfield video 
    using FFT, and determines the fraction of functional ciliated area 
    (FFCA) based on the percentage of pixels with PSDs exceeding a 
    specified power threshold. This implementation uses a compiled C#
    executable for the computationally expensive operations to speed
    up runtimes. 

    ARGUMENTS:
        video_path (str): Path to the AVI video to be processed.
        sampling_rate (int): Frame rate of the video.
        power_threshold (int): Minimum PSD value a pixel must exceed to 
            be considered ciliated.
        skip_existing (bool): whether a video should be skipped if a 
            MATLAB file already exists with the same name. 
        plot (bool): whether plots should be created and saved for 
            each video.

    RETURNS:
        avg_psd (np.ndarray): Average PSD curve across all pixels.
        psd_map (np.ndarray): PSD curve for each individual pixel.
        FFCA (float): Fraction of functional ciliated area in the video.
    """

    # First we'll generate the output path so we can check whether this
    # video has already been processed. 
    video_path_obj = Path(video_path)
    video_folder = video_path_obj.parent
    file_name = f'{video_path_obj.stem}_CBF_FFCA.mat'
    output_path = video_path_obj.parent / file_name

    # Skip this file if it already exists
    if os.path.exists(output_path) and skip_existing:
        print(f'{file_name} already exists. Skipping this video.')
        return

    # Open video
    print(f'Loading {video_path}...')
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f'ERROR: Cannot open video {video_path}')

    # Calculate some details
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fft_length = num_frames // 2 + 1

    # Reset cap read, just to be safe
    print('Converting to grayscale...')
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Preallocate array for grayscale frames
    grayscale_frames = np.zeros((num_frames, frame_height, frame_width), dtype=np.uint8)

    # Read and convert frames
    for i in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            break
        # Convert frame to grayscale using OpenCV
        grayscale_frames[i] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Import the cache folder to be used for storing bins locally
    from ..utilities import CACHE_FOLDER_PATH

    # Save the input frames to a binary file for access by the C# executable
    input_binary_path = os.path.join(CACHE_FOLDER_PATH, 'input.bin')
    output_binary_path = os.path.join(CACHE_FOLDER_PATH, 'psd_output.bin')
    
    # Save the grayscale frames to a binary file
    print('Saving to binary...')
    # grayscale_frames.astype(np.float32).tofile(input_binary_path)
    
    # Determine the path to the executable
    current_file = Path(__file__).resolve()

    # Construct path to the exe relative to this file
    # Assuming the structure: hilllab/cilia/FFTProcessor/FFTProcessor.exe
    executable_path = str(current_file.parent / "FFTProcessor" / "FFTProcessor.exe")

    # Call C# executable
    print('Launching executable...')
    start = time.time()
    subprocess.run([
        executable_path,
        str(input_binary_path),
        str(output_binary_path),
        str(num_frames),
        str(frame_height),
        str(frame_width),
        str(sampling_rate)
    ])

    # Load PSD map after execution
    psd_map = np.fromfile(output_binary_path, dtype=np.float32).reshape(frame_height, frame_width, fft_length)
    max_psd_map = np.max(psd_map, axis=2)

    print(f'\nFinished FFT analysis in {round(time.time() - start, 2)} seconds')

    # Now that we're outside of the loop, we can do some more calculations
    # First, we'll calculate the maximum power of each pixel
    print('Performing final calculations...')

    # And calculate the frequency vector so we can plot the PSD nicely
    frequency_vector = np.linspace(0, sampling_rate / 2, num_frames // 2 + 1)

    # Average all the PSDs together to get one PSD representative of the whole video
    avg_psd = np.mean(psd_map, axis=(0, 1))

    # Calculate the percent ciliation by counting how many are above a certain
    # power threshold (fraction of functional ciliated area). 
    flat_max_psds = max_psd_map.flatten()
    ffca = np.sum(flat_max_psds > power_threshold) / flat_max_psds.size
    ffca_map = (max_psd_map >= power_threshold).astype(int)

    # Create figure (if requested)
    if plot:
        fig = plt.figure(figsize=(10, 8))
        gs = gridspec.GridSpec(2, 2, height_ratios=[2, 1])  # 2 rows, 2 columns

        ax_top = fig.add_subplot(gs[0, :])
        ax_top.plot(frequency_vector, avg_psd)
        ax_top.set_title("Top long plot")
        ax_top.grid(True)
        ax_top.set_title(f'{video_path}\nCBF and FFCA')
        ax_top.set_xlabel('Frequency (Hz)')
        ax_top.set_ylabel('Power')

        ax_bottom1 = fig.add_subplot(gs[1, 0])
        ax_bottom1.set_title('Max PSD Power Map')
        ax_bottom1.imshow(max_psd_map)

        ax_bottom2 = fig.add_subplot(gs[1, 1])
        ax_bottom2.set_title('FFCA Map')
        ax_bottom2.imshow(ffca_map, cmap='RdGy_r')
        
    # Compile all the data
    mat_dict = {
        'freq': frequency_vector,
        'FFCA': ffca,
        'mens_CBF': avg_psd
    }

    # Save to MATLAB .mat file
    savemat(output_path, mat_dict)

    # Delete bin files from cache
    # xxx

    print('Finished processing!')

    return avg_psd, psd_map, ffca
