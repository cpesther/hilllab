# Christopher Esther, 2/27/2026
import os
from pathlib import Path
import pandas as pd
import cv2
import matplotlib.pyplot as plt

from ..utilities.warning import warn
from ..utilities.walk_dir import walk_dir
from ..utilities.print_progress_bar import print_progress_bar
from .masks.circular import circular
from .plot.contour_hist import contour_hist

def count_beads(folder, bead_type, radius_um, bead_area_range=(3, 40)):

    """
    Counts the number of beads in a set of runoff and bound images and 
    returns an Excel file with detailed counts.

    ARGUMENTS:
        folder (string): the path to the folder which contains a 
            'runoff' and 'bound' subfolder.
        bead_type (string): the type of bead used in the experiment. 
            Suggested values are 'COOH', 'Amine', 'PEG', or 'Other'. 
            This value is only stored in the Excel file and does not 
            affect processing.
        radius_um (float): the radius of the bead used in micrometers (µm). 
            This value is only stored in the Excel file and does not 
            affect processing.
        bead_area_range (tuple): the range of areas in pixels² of pixels
            that will be counted. The first number is the minimum area
            and the second area is the maximum area.
    """

    # Warn about the bead radius if a weird number was provided
    if (radius_um < 0.05) or (radius_um > 10):
        warn(msg='Bead radius should be provided in micrometers (um). ' \
                f'Check that your value of {radius_um} µm is correct.')

    # List everything within this folder
    all_files = os.listdir(folder)

    # Create lookup dict using all caps versions for case insensitivity
    subfolder_lookup = {sf.upper(): sf for sf in all_files}

    # Ensure that a runoff and bound subfolder are present
    if 'BOUND' not in subfolder_lookup.keys():
        raise OSError('Bound folder not found.')
        return None
        
    if 'RUNOFF' not in subfolder_lookup.keys():
        raise OSError('Runoff folder not found.')
        return None

    # Create the folder for plots and annotated images
    annotated_folder = Path(folder) / 'annotated'
    plots_folder = Path(folder) / 'plots'
    annotated_folder.mkdir(parents=True, exist_ok=True)
    plots_folder.mkdir(parents=True, exist_ok=True)

    # Create a DataFrame for storing the results
    results = pd.DataFrame(columns=['path', 'file', 'slide', 'n_small', 'n_expected', 
                                    'n_large', 'radius_um', 'bead_type', 'bead_area_range_low', 
                                    'bead_area_range_high'])

    # Now we'll work in each subfolder individually
    subfolders = ['RUNOFF', 'BOUND']
    for subfolder in subfolders:
        
        # Get the full path to this subfolder
        subfolder_name = subfolder_lookup[subfolder]
        subfolder_path = os.path.join(folder, subfolder_name)

        # List all images in this subfolder
        all_subfolder_files = walk_dir(subfolder_path, extension=['png', 'jpg', 'jpeg', 'tiff'])
        n_subfolder_files = len(all_subfolder_files)

        # Verify files found 
        if len(all_subfolder_files) == 0:
            raise OSError(f'No images found in {subfolder_path}')

        # Here's the processing loop as we work through each file
        for i, file in enumerate(all_subfolder_files):

            # Pull file name
            file_name = Path(file).stem
            
            # Print progress bar
            print_progress_bar(progress=i+1, total=n_subfolder_files, 
                               title=f'Processing {subfolder.capitalize()}')

            # Read the image in grayscale
            gray = cv2.imread(file, 0)
            if gray is None:
                warn(f'Could not read image {file}')
                continue  # go to next if unable to read this image

            # Apply mask to eliminate artifacts outside well that could 
            # distract bead counting.
            masked_gray = circular(gray)

            # Blurring helps eliminate small artifacts or variations
            gray_blurred = cv2.GaussianBlur(masked_gray, (5, 5), 0)

            # Thresholding sets any pixel with any brightness to maximum values for easier counting
            _, threshed = cv2.threshold(gray_blurred, 1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

            # Now we'll find the contours within this image
            contours = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]

            # Create an annotated image that can be used for nice display
            annotated_img = cv2.cvtColor(masked_gray, cv2.COLOR_GRAY2BGR)

            # Draw circular mask boundary in magenta on annotated image
            height, width = gray.shape
            center = (width // 2, height // 2)
            radius = min(center) - 10
            cv2.circle(annotated_img, center, radius, (255, 0, 255), 5)

            # Count contours of different sizes
            counts = {
                'small': [],
                'expected': [],
                'large': []
            }
            
            # For each contour that was found
            for contour in contours:
            
                # Calculate the area in pixels squared
                area = cv2.contourArea(contour)
            
                # Sort contours based on area
                if area < bead_area_range[0]:
                    cv2.drawContours(annotated_img, [contour], -1, (100, 0, 0), 4)
                    cv2.drawContours(annotated_img, [contour], -1, (255, 0, 0), 2)
                    counts['small'].append(area)
                    
                elif bead_area_range[0] <= area <= bead_area_range[1]:
                    cv2.drawContours(annotated_img, [contour], -1, (0, 100, 0), 4)
                    cv2.drawContours(annotated_img, [contour], -1, (0, 255, 0), 2)
                    counts['expected'].append(area)
                
                elif area > bead_area_range[1]:
                    cv2.drawContours(annotated_img, [contour], -1, (0, 0, 100), 4)
                    cv2.drawContours(annotated_img, [contour], -1, (0, 0, 255), 2)
                    counts['large'].append(area)

            # Draw contours onto the annotated image
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.imshow(annotated_img)
            ax.set_title(file)
            fig.patch.set_facecolor('black')
            ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
            ax.set_title(f'{file}\n', color='gray')

            # Create a legend for the annotated image        
            legend_elements = [
                plt.Rectangle((0,0),1,1, color='#FF00FF', label='Mask'),
                plt.Rectangle((0,0),1,1, color='#FF0000', label='Small'),
                plt.Rectangle((0,0),1,1, color='#00FF00', label='Expected'),
                plt.Rectangle((0,0),1,1, color='#0000FF', label='Large')
            ]
            ax.legend(handles=legend_elements, frameon=False, labelcolor='white')

            # Save annotated image to its folder
            annotated_save_path = annotated_folder / f'{Path(file).stem}_{subfolder.lower()}.png'
            plt.savefig(annotated_save_path, facecolor='black', bbox_inches='tight', 
                        pad_inches=0.5, dpi=300)
            plt.close()

            # Contour classification histogram
            counts_hist_save_path = plots_folder / f'contourhist_{file_name}.png'
            contour_hist(counts=counts, file=file, save_path=counts_hist_save_path)
            plt.close()
            
            # Add results row to DataFrame
            results.loc[len(results)] = {
                'path': file,
                'file': file_name,
                'slide': subfolder.lower(),
                'n_small': len(counts['small']),
                'n_expected': len(counts['expected']),
                'n_large': len(counts['large']),
                'radius_um': radius_um,
                'bead_type': bead_type,
                'bead_area_range_low': bead_area_range[0],
                'bead_area_range_high': bead_area_range[1]   
            }

        # To prevent weird progress bar stacking
        print('\n')

    # Save results to Excel for this date
    excel_path = Path(folder) / f'{Path(folder).name}_counts.xlsx'
    results.to_excel(excel_path, index=False)
    print(f'\nCounts saved to {excel_path}')
    return results
