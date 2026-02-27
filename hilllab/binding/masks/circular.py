# Christopher Esther, Hill Lab, 2/27/2026
import cv2
import numpy as np

# Function to apply circular mask to an image
def circular(image, margin=10):

    """
    Apply a centered circular mask to an image and return the masked result.

    This function creates a binary mask with a filled circle positioned at the
    image center. The circle radius is set to the largest value that fits inside
    the image while leaving a given margin. Pixels outside the circle are
    set to black, while pixels inside remain unchanged.

    ARGUMENTS:
        image (numpy.ndarray): input image array of shape (H, W) or (H, W, C)
        margin (int): the number of pixels by which the radius of the 
            mask will be reduced as compared to the total width and
            height of the image. 

    RETURNS:
        masked_image (numpy.ndarray): image of the same shape as the input 
            where only the circular region remains visible and all other pixels 
            are zeroed out.
    """

    # Calculate height and width of image and location of center
    height, width = image.shape[:2]
    center = (width // 2, height // 2)

    # Radius is the minimum of width and height minus the margin
    radius = min(center) - margin

    # Create 2D array of all zeroes
    mask = np.zeros((height, width), dtype=np.uint8)

    # Set circular region to maximum
    cv2.circle(mask, center, radius, 255, -1)

    # Apply and return mask
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    return masked_image
