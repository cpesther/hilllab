# Christopher Esther, Hill Lab, 1/22/2026
import cv2
from pathlib import Path
import os
import numpy as np

def bin_video(video_path, bin_size):

    """
    Bins each pixel in a video into a group of a specified size, outputting
    a video of smaller dimensions.
    """

    # Open the video and calculate a few things
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f'Cannot open video: {video_path}')

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Compute cropped dimensions that fit clean bins
    new_width = (width // bin_size) * bin_size
    new_height = (height // bin_size) * bin_size
    out_width = new_width // bin_size
    out_height = new_height // bin_size

    # Determine the output path
    output_name = f'BINx{bin_size}_{Path(video_path).stem}.avi'
    output_path = os.path.join(Path(video_path).parent, output_name)

    # Create the video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    writer = cv2.VideoWriter(output_path, fourcc, fps, (out_width, out_height))

    # Verify the video writer
    if not writer.isOpened():
        cap.release()
        raise ValueError(f'Cannot open VideoWriter: {output_path}')
    
    # Perform the binning
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Crop to bin-compatible size
        frame = frame[:new_height, :new_width]

        # Reshape into bins and average
        h, w, c = frame.shape
        frame = frame.reshape(h // bin_size, bin_size, w // bin_size, bin_size, c)
        frame = frame.mean(axis=(1, 3)).astype(np.uint8)

        writer.write(frame)

    cap.release()
    writer.release()
    print(f'Saved binned video to: {output_path}')
    return output_path
