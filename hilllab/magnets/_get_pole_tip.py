# Christopher Esther, Hill Lab, 11/20/2025
import cv2

def _get_pole_tip(image):
    """
    Allows the user to select the location of the pole tip on an image.
    Returns the coordinates as a tuple (x, y) of the most recent click.
    """
    pole_tip = [None]  # Use a list to store a single click

    def click_event(event, x, y, flags, params):
        """
        Callback function for mouse events.
        Updates pole_tip with the coordinates of the latest left-button click.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            pole_tip[0] = (x, y)  # Overwrite with the latest click
            print(f'Pole tip selected at {pole_tip[0]}. Close window to confirm.')

    # Create a resizable window
    window_name = 'Select pole tip, then close to confirm.'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 800, 600)

    # Display the image
    cv2.imshow(window_name, image)
    print('Click on the image to select the tip of the cantilever and then close the window to proceed.')

    # Set the mouse callback
    cv2.setMouseCallback(window_name, click_event)

    # Wait for a key press
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(f'Pole tip confirmed at {pole_tip[0]}')
    
    # Return the latest clicked coordinates
    return pole_tip[0]
