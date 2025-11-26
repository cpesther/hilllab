import numpy as np
import cv2

def get_pole_tip(Image): 
    poleTip = [] 
    def click_event(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            # print(f"Clicked at: x={x}, y={y}")
            # Save the coordinates to a file
            poleTip.append(x)
            poleTip.append(y) 


    
    cv2.imshow("Image", Image)
    print("Click on the image to select the tip of the cantilever and then close to proceed.")
    cv2.setMouseCallback("Image", click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return tuple(poleTip)


def find_origin_from_lines(lines):
    
    """
    Finds the best-fit origin (point) from a set of radially distributed 
    lines using a least-squares solution.

    ARGUMENTS:
        lines (list of tuples): Each tuple contains the start and end
            points of a line, e.g., ((x1, y1), (x2, y2)).

    RETURNS:
        tuple: The (x, y) coordinates of the best-fit origin.
    """

    # At least two lines are required. 
    if len(lines) < 2:
        return None  # At least two lines are required.

    # Build the system of linear equations A * p = b
    # where p is the point (x, y) we want to find.
    A = []
    b = []

    for line in lines:
        (x1, y1), (x2, y2) = line

        # Calculate the direction vector of the line.
        dx = x2 - x1
        dy = y2 - y1

        # Compute the Hessian normal form of the line.
        # This is a robust way to handle vertical lines.
        # The equation of the line is a*x + b*y + c = 0.
        a = dy
        b_coeff = -dx
        c = -dy * x1 + dx * y1

        # Append to our matrix and vector.
        A.append([a, b_coeff])
        b.append(-c)

    A_matrix = np.array(A)
    b_vector = np.array(b)

    # Solve the overdetermined system of linear equations using least squares.
    # The result is the point (x, y) that minimizes the sum of squared distances.
    try:
        origin, residuals, rank, singular_values  = np.linalg.lstsq(A_matrix, b_vector, rcond=None)
        return tuple(origin)
    except np.linalg.LinAlgError:
        # Handle case where lines are all parallel or have issues.
        print("Could not find a valid origin.") 
        return None


def delete_wide_angled_points(df, origin, poletip, angle_threshold):
    """
    Deletes points from a DataFrame that have angles with origin and poletip axis wider than the specified threshold.

    Args:
        df (DataFrame): DataFrame containing 'x', 'y', and 'frame' columns.
        angle_threshold (float): Angle threshold in degrees. Points with angles
    """
    vec_axis =  np.array(poletip) - np.array(origin)

    df_narrow = []
    for idx, row in df.iterrows():
        vec_point = np.array([row['x'], row['y']]) - np.array(origin)
        cos_theta = np.dot(vec_point, vec_axis) / (np.linalg.norm(vec_point) * np.linalg.norm(vec_axis))
        theta = np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))
        df_narrow[idx] = row if theta <= angle_threshold else None

    df_narrow.columns = ['frame','particle','y','x']
    
    return df_narrow



def get_force_vs_distance_relationships(data, viscosity, origin, diameter): # Assuming data is sorted in time and has ('t', 'x', 'y', 'PID', 'voltage')
    
    Coeff_at_Voltages = []   # coefficients (m,c) go into log(force) = m*log(distance) + c
    distance = []
    force = []

    for voltage in np.array(data['voltage'].unique()): # voltage are actually not repeated in the recommended calibration matrix by DJC 
        init_time = data[data['voltage'] == voltage].iloc[0]['t']                     # may want to set this time to a bit later than the first frame to consider constant velocity only  
        final_time = data[data['voltage'] == voltage].iloc[-1]['t']
        
        data_init = data[(data['voltage'] == voltage) & (data['t'] == init_time)]     # information at initial frame or time stamp for this voltage        
        data_final = data[(data['voltage'] == voltage) & (data['t'] == final_time)]   # information at final frame or time stamp for this voltage

        for PID in np.sort(data_init['PID']): # PID at this frame number or time stamp should be unique anyway  
            
            if PID in data_final['PID'].values:
                # distance estimation
                (y1, x1) = data_init[data_init['PID']==PID].iloc[['y', 'x']]       # Initial position
                (y2, x2) = data_final[data_final['PID']==PID].iloc[['y', 'x']]     # Final position

                # Stokes' drag force calculation
                velocity = np.sqrt((x2 - x1)**2 + (y2 - y1)**2) / (final_time - init_time)  # Velocity
                force = 3 * np.pi * viscosity * diameter * velocity  # under constant velocity, stokes' drag force = force applied 
        
                distance.append((origin[0] - np.mean([x1,x2]))**2 + (origin[1]-np.mean(y1,y2))**2)
                force.append(force) 
        
        ### fit log(force)-log(distance) eqn to all the points found at this voltage to get the coefficients
        m , c = np.polyfit(np.log(distance), np.log(force), 1)

        Coeff_at_Voltages.append((voltage, m, c)) # (m,c) coefficients of log-log fit
    
    return Coeff_at_Voltages