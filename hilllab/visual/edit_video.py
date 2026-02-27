# Christopher Esther, Hill Lab, 2/27/2026
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def edit_video(video_path, output_path, brightness=0, contrast=1.0, gamma=1.0, 
               saturation=1.0, sharpness=0.0, codec='XVID', show_preview=False):

    """
    Applies various parameter edits to a video including brightness, 
    contrast, gamma, saturation, and sharpness. 

    ARGUMENTS:
        video_path (string): the path to the video to be edited
        output_path (string): the full path where the edited video 
            should be saved.
        brightness (int, optional): value added to each pixel intensity.
            Negative values darken the image, positive values brighten it.
            Recommended range is -100 to 100. Default is 0.
        contrast (float, optional): scales difference between light and dark
            regions. Values above 1 increase contrast while values between
            0 and 1 decrease it. Recommended range is 0.5 to 2.0. Default is 1.0.
        gamma (float, optional): nonlinear brightness correction factor.
            Values below 1 brighten shadows, values above 1 darken shadows.
            Recommended range is 0.5 to 2.5. Default is 1.0.
        saturation (float, optional): multiplies color intensity.
            Values above 1 increase color vividness, values between 0 and 1
            reduce saturation. A value of 0 produces grayscale. Recommended
            range is 0 to 3. Default is 1.0.
        sharpness (float, optional): controls edge enhancement strength.
            Higher values increase edge contrast and detail but may introduce
            noise or artifacts. Recommended range is 0 to 2. Default is 0.0.
        codec (string, optional): four character video codec identifier used
            for encoding the output video. Must be supported by the system's
            OpenCV build. Default is 'XVID'.
        show_preview (bool, optional): if True, displays the first frame of the
            video side by side before and after edits using matplotlib before
            processing begins allowing user to confirm. Default is False.
    """

    # Try to find and open the video
    if not os.path.exists(video_path):
        raise FileNotFoundError('Input video not found')

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError('Could not open video')

    # Calculate a few video parameters
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    # Create and verify the video writer object
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), True)

    if not out.isOpened():
        cap.release()
        raise ValueError('Could not create output video')

    # Calculate a gamma table
    inv_gamma = 1.0 / gamma
    gamma_table = np.array([(i / 255.0) ** inv_gamma * 255 for i in range(256)]).astype('uint8')

    # Create a helper function for applying edits to a frame
    def apply_edits(frame):
        frame = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)

        if gamma != 1.0:
            frame = cv2.LUT(frame, gamma_table)

        if saturation != 1.0:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype('float32')
            hsv[:, :, 1] *= saturation
            hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
            frame = cv2.cvtColor(hsv.astype('uint8'), cv2.COLOR_HSV2BGR)

        if sharpness > 0:
            blur = cv2.GaussianBlur(frame, (0, 0), 3)
            frame = cv2.addWeighted(frame, 1 + sharpness, blur, -sharpness, 0)

        return frame

    # Preview first frame, if requested
    if show_preview:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            out.release()
            raise ValueError('Could not read first frame')

        edited = apply_edits(frame.copy())

        # Convert BGR to RGB for matplotlib
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        edited_rgb = cv2.cvtColor(edited, cv2.COLOR_BGR2RGB)

        # Show changes side by side in matplotlib
        plt.figure(figsize=(10,5))
        plt.subplot(1,2,1)
        plt.title('Original')
        plt.imshow(frame_rgb)
        plt.axis('off')

        plt.subplot(1,2,2)
        plt.title('Edited')
        plt.imshow(edited_rgb)
        plt.axis('off')

        plt.tight_layout()
        plt.show()

        # Ask for user confirmation
        confirmation = input('Proceed with edits? [y]/n: ').upper()
    
    # If no preview created, confirmation is implied
    else:
        confirmation = 'Y'
        
    # If agreeing to proceed, apply edits
    if confirmation in ['Y', '']:

        # Rewind to beginning
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # Apply edits
        while True:
            ret, frame = cap.read()
            if not ret:
                break
        
            frame = apply_edits(frame)
            out.write(frame)

    # Close down all the readers and writers
    cap.release()
    out.release()
