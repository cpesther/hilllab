# Christopher Esther, Hill Lab, 11/20/2025
import glob
import os
import cv2
from pathlib import Path
from ..utilities.print_progress_bar import print_progress_bar

def images_to_video(image_folder, fps=30):

    """
    Takes a folder full of PNGs or JPGs and converts them into an AVI video.

    ARGUMENTS:
        image_folder (string): the path to the folder filled with images
        fps (int): the frame rate of the resultant video
    """
    
    # Grab all JPG and PNG files
    images = sorted(
        glob.glob(os.path.join(image_folder, "*.jpg")) 
        + glob.glob(os.path.join(image_folder, "*.png"))
    )

    if not images:
        raise ValueError("No images found in the folder.")

    # Read the first image to get frame dimensions
    frame = cv2.imread(images[0])
    if frame is None:
        raise ValueError("Unable to read the first image.")
    height, width, _ = frame.shape

    # Get the name of the folder to use as the video name
    video_name = f'{Path(image_folder).stem}.avi'
    output_path = os.path.join(image_folder, video_name)
    
    # Define the codec and create the video writer
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Add each frame to the video
    for index, img_path in enumerate(images):

        # Print a progress bar too
        print_progress_bar(progress=index+1, total=len(images), title='Building video')
        img = cv2.imread(img_path)
        if img is None:
            continue
        resized = cv2.resize(img, (width, height))
        video_writer.write(resized)

    video_writer.release()
    print(f'\nSuccessfully exported {video_name}')
