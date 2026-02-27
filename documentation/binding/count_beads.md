# count_beads()
_hilllab.binding.count_beads()_

Counts the number of beads in a set of runoff and bound images and returns an Excel file with detailed counts.

_See also [batch_count_beads()](batch_count_beads.md)_

### _Arguments_
- __`folder` : string__  
    The path to the folder which contains a 'runoff' and 'bound' subfolder. 

- __`bead_type` : string__  
    The type of bead used in the experiment. Suggested values are 'COOH', 'Amine', 'PEG', or 'Other'. This value is only stored in the Excel file and does not affect processing.

- __`bead_radius_um` : float or int__  
    The radius of the bead used in micrometers (µm). This value is only stored in the Excel file and does not affect processing.

- __`method` : string, default 'OLY'__  
    The method that was used to capture the images, which affects how they are processed. Must be one of the values below:
    - 'OLY': 

### _Returns_
This function does not return any variables. 

### _File Outputs_
- __Excel__ (.xlsx): an Excel file containing the bead counts for each image in the bound and runoff folders. 
- __Folder__: 

### _Notes_
- The `folder` path must contain both a folder named 'runoff' and a folder named 'bound' which each contain images with beads. The capitalization of the folder names does not matter. 
- For best results, each bound and runoff image pair should share the exact same name (just be stored in the separate folders). This will enable automatic matching between bound and runoff images for plotting. 
- The function can work with images in PNG, JPG, JPEG, or TIFF formats. 
