# Christopher Esther, Hill Lab, 10/13/2025
import os
from pathlib import Path
import numpy as np
import cv2
import time
import gc

from ..utilities.print_progress_bar import print_progress_bar
from ._resolve_CBF_FFCA import _resolve_CBF_FFCA

def _calculate_CBF_FFCA_py(video_path, sampling_rate=60, power_threshold=5, 
                       skip_existing=True, plot=False):

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
    file_name = f'{video_path_obj.stem}_CBF_FFCA.csv'
    output_path = video_path_obj.parent / file_name

    # Skip this file if it already exists
    if os.path.exists(output_path) and skip_existing:
        print(f'{file_name} already exists. Skipping this video.')
        return None, None

    # Open video
    print(f'Loading {video_path}...')
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f'ERROR: Cannot open video {video_path}')

    # Calculate some details
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

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
    # that we can squeeze every bit of memory out of the machine that we can
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
        print_progress_bar(progress=row+1, total=frame_height, title='Performing FFT', multiple=2)
        
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

    # Resolve the actual CBF and FFCA values here
    cbf, ffca = _resolve_CBF_FFCA(psd_map=psd_map, frequency_vector=frequency_vector,
                                  power_threshold=power_threshold, output_path=output_path)
    
    print('Finished processing!')

    return cbf, ffca
