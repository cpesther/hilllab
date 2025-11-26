# Christopher Esther, Hill Lab, 11/20/2025
import numpy as np

def _remove_wide_angles(df, origin, pole_tip, angle_threshold):
    
    """
    Deletes particles from a DataFrame that have an angle with the 
    origin/poletip axis wider than the specified threshold.

    Args:
        df (DataFrame): DataFrame containing 'x', 'y', and 'frame' columns.
        angle_threshold (float): Angle threshold in degrees. Points with angles
    """

    # Compute the reference axis from origin to pole tip
    axis_vector = np.array(pole_tip) - np.array(origin)

    # Ensure axis_vector is not zero-length
    if np.linalg.norm(axis_vector) == 0:
        raise ValueError("Pole tip and origin are the same point; axis vector has zero length.")

    # Convert axis_vector to a unit vector for efficiency
    axis_unit = axis_vector / np.linalg.norm(axis_vector)

    # Extract particle coordinates as an array
    coords = df[['x', 'y']].to_numpy()
    vectors_to_points = coords - np.array(origin)  # vectors from origin to points

    # Compute cosine of angles using dot product formula
    dot_products = np.dot(vectors_to_points, axis_unit)
    norms = np.linalg.norm(vectors_to_points, axis=1)
    cos_theta = dot_products / norms

    # Clip values to [-1, 1] to avoid numerical errors in arccos
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    angles = np.degrees(np.arccos(cos_theta))

    # Filter rows where angle <= threshold
    mask = angles <= angle_threshold
    df_cleaned = df[mask].copy()  # keep only rows within the allowed angle

    return df_cleaned
