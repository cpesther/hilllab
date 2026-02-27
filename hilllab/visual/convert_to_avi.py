# Christopher Esther, Hill Lab, 2/27/2026
import os
import cv2

def convert_to_avi(video_path, output_path, grayscale=False, codec='XVID'):

    """
    Converts a video to an AVI file, with the option to also convert it
    into grayscale. 

    ARGUMENTS:
        video_path (string): the path to the video
        output_path (string): the full output path where the converted
            video will be saved. Should end with .avi. 
        grayscale (bool): whether the video should be converted to
            grayscale. 
        codec (string, default 'XVID'): the coded used for the converted
            video
    """

    # Try to open the video
    if not os.path.exists(video_path):
        raise FileNotFoundError('Input video not found')

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError('Could not open video file')

    # Calculate a few important attributes
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    # Create the output video writer object
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height),
        isColor=not grayscale
    )

    # Fail if unable to create output writer
    if not out.isOpened():
        cap.release()
        raise ValueError('Could not open VideoWriter')

    # For every frame in the video
    while True:

        # Read the next frame, break if there isn't one
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale, if requested
        if grayscale:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Write teh frame
        out.write(frame)

    # Close the video readers and writers
    cap.release()
    out.release()
    