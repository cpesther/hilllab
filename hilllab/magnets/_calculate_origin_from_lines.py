# Christopher Esther, Hill Lab, 11/20/2025
import numpy as np

def _calculate_origin_from_lines(lines):
    """
    Estimate the best-fit origin from a set of radial lines using least squares.

    ARGUMENTS:
        lines (list of tuples): Each element is a line segment defined by
            start and end points: ((x_start, y_start), (x_end, y_end)).

    RETURNS:
        tuple or None: (x, y) coordinates of the estimated origin,
        or None if a valid origin cannot be determined.
    """

    # At least two vectors are required to determine an intersection
    if len(lines) < 2:
        raise ValueError('Need at least two lines to determine an origin.')

    # Lists to construct the linear system A * [x, y]^T = b
    line_coefficients = []  # Stores the [a, b] coefficients for each line in Hessian form
    constants_vector = []   # Stores the -c values for each line

    # Loop through each line segment
    for line_index, line in enumerate(lines):
        (x_start, y_start), (x_end, y_end) = line

        # Compute the direction vector of the line
        delta_x = x_end - x_start
        delta_y = y_end - y_start

        # Convert the line to Hessian normal form: a*x + b*y + c = 0
        # a = dy, b = -dx, c = -(a*x1 + b*y1)
        # This formulation handles vertical and horizontal lines without slope issues
        a = delta_y
        b = -delta_x
        c = -(a * x_start + b * y_start)

        # Append coefficients and constants to the system
        line_coefficients.append([a, b])
        constants_vector.append(-c)
        
    # Convert lists to NumPy arrays for linear algebra
    A_matrix = np.array(line_coefficients)
    b_vector = np.array(constants_vector)

    try:
        # Solve the overdetermined system using least squares
        # This finds the point (x, y) that minimizes the sum of squared distances
        origin_point, residuals, rank, singular_values = np.linalg.lstsq(A_matrix, b_vector, rcond=None)
        return tuple(origin_point)

    except np.linalg.LinAlgError:
        # This occurs if the system is degenerate (e.g., all lines are parallel)
        print("ERROR: Could not determine a valid origin; check if lines are degenerate or parallel.")
        return None
