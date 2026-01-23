# Christopher Esther, Hill Lab, 1/22/2026
import os
import cv2

def extract_frame(video_path, output_folder, frame_index=0, scale_percent=100):
    
    """
    Extracts the a frame of a given index from a video and saves it as 
    a PNG in the specified folder.

    Parameters:
        video_path (str): Path to the AVI video file.
        output_folder (str): Folder to save the PNG.
        frame_index (int): the 0-based index of the frame to be saved
        scale_percent (float): Percentage to downscale the frame (default 100 = no scaling).
    """
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Load video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f'Cannot open video: {video_path}')
    
    # Set target frame number (0-based index)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    
    # Read the requested frame
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise ValueError(f'Cannot read frame {frame_index} of video: {video_path}')
    
    # Resize frame if needed
    if scale_percent != 100:
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
    
    # Build output path with same name as video but include frame number
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_path = os.path.join(output_folder, f'{base_name}_frame{frame_index}.png')
    
    # Save frame as PNG
    cv2.imwrite(output_path, frame)
    print(f'Saved frame {frame_index} to: {output_path}')
    return frame
