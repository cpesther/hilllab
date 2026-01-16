# Christopher Esther, Hill Lab, 1/9/2026
import cv2
import numpy as np
from pathlib import Path

from ..visual.calculate_mean_brightness import calculate_mean_brightness

def normalize_video_brightness(video_path, normalized_brightness, n_samples=5):

    """
    Normalizes the mean brightness of a grayscale video to a specific value.
    
    ARGUMENTS:
        video_path (str): the path to the video to be normalized
        normalized_brightness (int): the mean brightness to which the 
            video should be normalized. Any value between 0 and 255.
        n_samples (int): the number of evenly spaced samples that should
            be taken to determine the brightness of the video before
            normalization. 
    """

    # Create the video object
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Could not open video file: {video_path}")
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        cap.release()
        raise ValueError("Video contains no frames")
    
    # Determine the indices of frames to use for sampling
    indices = np.linspace(0, total_frames - 1, n_samples, dtype=int)
    
    # Load sample frames
    sample_frames = []
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue
        sample_frames.append(frame)
    
    cap.release()
    
    # Calculate mean brightness in each sample frame
    brightness_values = []
    for frame in sample_frames:
        brightness_values.append(calculate_mean_brightness(frame=frame))

    # Calculate video brightness and normalization factor
    video_brightness = np.mean(brightness_values)
    factor = normalized_brightness / video_brightness

    # Now reopen and adjust the video and save a copy
    output_video_name = 'NORM_' + Path(video_path).name
    output_video_path = Path(video_path).parent / output_video_name
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
    
        adjusted = np.clip(frame.astype(np.float32) * factor, 0, 255)
        out.write(adjusted.astype(np.uint8))
    
    cap.release()
    out.release()
    