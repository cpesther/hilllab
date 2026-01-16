# Christopher Esther, Hill Lab, 12/19/2025
import cv2
import numpy as np

def calculate_mean_brightness(video_path=None, frame=None):

    """
    Calculates the mean brightness of the first frame of a video after 
    conversion to grayscale.

    ARGUMENTS:
        video_path (string): the path to the video file
        frame (numpy.array): 2D array of values 

    RETURNS:
        mean_brightness (float): the mean brightness of every pixel in 
            the first frame of the video
    """

    if (frame is None) and (video_path is None):
        print('ERROR: Neither a video path nor frame was provided.')

    # If a frame wasn't provided, open the video 
    if frame is None:

        # Open the video
        cap = cv2.VideoCapture(video_path)

        # Read the first frame
        ret, frame = cap.read()

        if not ret:
            raise RuntimeError('Failed to read the first frame from the video.')

        # Release the video capture
        cap.release()
            
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate the average brightness
    mean_brightness = np.mean(gray_frame)

    return mean_brightness
