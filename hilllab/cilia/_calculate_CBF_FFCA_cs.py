# Christopher Esther, Hill Lab, 10/13/2025
import os
from pathlib import Path
import numpy as np
import time
import subprocess

from ..cilia._resolve_CBF_FFCA import _resolve_CBF_FFCA

def _calculate_CBF_FFCA_cs(video_path, sampling_rate=60, power_threshold=1, 
                          skip_existing=True, delete_process_files=True):

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
        delete_process_files (bool): If true, the binary files created by the
            FFTProcessor.exe will be deleted once finished to free up 
            disk space. 
    """

    # First we'll generate the output path so we can check whether this
    # video has already been processed.
    video_path_obj = Path(video_path)
    video_name = video_path_obj.stem
    video_folder = video_path_obj.parent
    print(f'Starting processing on {str(video_path_obj)}')
    file_name = f'{video_path_obj.stem}_CBF_FFCA.csv'
    output_path = video_path_obj.parent / file_name

    # Skip this file if it already exists
    if os.path.exists(output_path) and skip_existing:
        print(f'{file_name} already exists. Skipping this video.')
        return None, None

    # Save the input frames to a binary file for access by the C# executable
    psd_binary_path = os.path.join(video_folder, f'{video_name}_psd_map.bin')
    freq_binary_path = os.path.join(video_folder, f'{video_name}_freq_map.bin')
    meta_path = os.path.join(video_folder, f'{video_name}_meta.txt')
        
    # Determine the path to the FFTProcessor executable
    current_file = Path(__file__).resolve()

    # Construct path to the exe relative to this file
    executable_path = str(current_file.parent / "FFTProcessor" / "FFTProcessor.exe")

    # Compile the arguments
    arguments = [executable_path, str(video_path), str(psd_binary_path), 
                 str(freq_binary_path), str(meta_path), str(sampling_rate), 'false']

    # Call C# executable
    print('Running FFTProcessor.exe...')
    start = time.time()

    try:
        result = subprocess.run(
            arguments,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        # Print EXE output
        print(result.stdout)
        if result.stderr:
            print("EXE stderr:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"EXE failed with return code {e.returncode}")
        print("stdout:", e.stdout)
        print("stderr:", e.stderr)

    print(f'\nFinished FFT analysis in {round(time.time() - start, 2)} seconds')

    # Load metadata from text file
    with open(meta_path, "r") as f:
        num_frames = int(f.readline())
        frame_height = int(f.readline())
        frame_width = int(f.readline())
    fft_length = num_frames // 2 + 1

    # Load maps from binaries
    psd_map = np.fromfile(psd_binary_path, dtype=np.float32).reshape(frame_height, frame_width, fft_length)

    # Now we can perform some final calcuations
    print('Performing final calculations...')
    frequency_vector = np.linspace(0, sampling_rate / 2, num_frames // 2 + 1)

    # Resolve the actual CBF and FFCA values here
    cbf, ffca = _resolve_CBF_FFCA(psd_map=psd_map, frequency_vector=frequency_vector,
                                  power_threshold=power_threshold, output_path=output_path)
    
    # Delete the binary files, if requested
    if delete_process_files:
        try:
            os.remove(psd_binary_path)
            os.remove(freq_binary_path)
            os.remove(meta_path)
        except Exception:
            pass

    print(f'Finished processing {Path(video_path).name}')
    return cbf, ffca
