# Christopher Esther, Hill Lab, 10/13/2025
from pathlib import Path
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time
from scipy.io import savemat
import pandas as pd
import gc

from ..utilities.print_progress_bar import print_progress_bar

def calculate_CBF_FFCA(video_path, sampling_rate=60, power_threshold=5, output_format='matlab', 
                       plot=False):

    """
    Calculates the ciliary beat frequency (CBF) from a brightfield video 
    using FFT, and determines the fraction of functional ciliated area 
    (FFCA) based on the percentage of pixels with PSDs exceeding a 
    specified power threshold.

    ARGUMENTS:
        video_path (str): Path to the AVI video to be processed.
        sampling_rate (int): Frame rate of the video.
        power_threshold (int): Minimum PSD value a pixel must exceed to 
            be considered ciliated.
        output_format (str): 'matlab' or 'none', indicating how the 
            results should be saved.
        plot (bool): whether plots should be created and saved for 
            each video.

    RETURNS:
        avg_psd (np.ndarray): Average PSD curve across all pixels.
        psd_map (np.ndarray): PSD curve for each individual pixel.
        FFCA (float): Fraction of functional ciliated area in the video.
    """

    # Open video
    print(f'Loading {video_path}...')
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f'ERROR: Cannot open video {video_path}')

    # Calculate some details
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Region of interest (ROI): full frame (can be modified for manual selection)
    roi_x = np.arange(frame_width)
    roi_y = np.arange(frame_height)

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

    grayscale_frames_float = grayscale_frames.astype(np.float32)  # convert to float

    # This script is memory intensive; you're gonna see a lot of deletes so 
    # that we can squeeze every bit of memory out of the maching that we can
    del cap
    del grayscale_frames
    gc.collect()  # also force garbage collection

    # Preallocate arrays for results
    print('Allocating memory...')
    fft_length = num_frames // 2 + 1  # keep only first half b/c second half is redundant
    psd_map = np.zeros((frame_height, frame_width, fft_length), dtype=np.float16)  # float16 less precise, but half the size
    max_psd_map = np.zeros((frame_height, frame_width), dtype=np.float32)

    # Run the actual iteration over each time series provided
    start = time.time()
    for row in range(frame_height):  # y-coordinate

        # Put our progress bar here
        print_progress_bar(progress=row, total=frame_height, title='Performing FFT', multiple=2)
        
        for column in range(frame_width):  # x-coordinate
            
            # Calculate the FFT
            pixel_ts = grayscale_frames_float[:, row, column]  # pull the time series
            norm_pixel_ts = pixel_ts - np.mean(pixel_ts)       # normalize it to its mean
            fft_result = np.fft.fft(norm_pixel_ts) 
            fft_result_trimmed = fft_result[:fft_length]       # take only first half

            # Calculate the PSD
            psd = (1 / (num_frames * sampling_rate)) * np.abs(fft_result_trimmed) ** 2
            psd[1:-1] *= 2  # correct amplitude for 1-sided PSD
            psd[:15] = 0    # remove very low frequencies

            # Save the data 
            psd_map[row, column, :] = psd
            max_psd_map[row, column] = np.max(psd)

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

    # Save the data in the requested format
    if output_format == 'matlab':
        
        # Compile all the data
        mat_dict = {
            'freq': frequency_vector,
            'FFCA': ffca,
            'mens_CBF': avg_psd
        }

        # Determine the path to the save file
        video_path_obj = Path(video_path)
        file_name = f'{video_path_obj.stem}_CBF_FFCA.mat'
        output_path = video_path_obj.parent / file_name

        # Save to MATLAB .mat file
        savemat(output_path, mat_dict)

    print('Finished processing!')

    return avg_psd, psd_map, ffca
