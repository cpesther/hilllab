# Christopher Esther, Hill Lab, 12/19/2025
from pathlib import Path
import os
import shutil

def publish():

    """
    Just a utility function to move the FFTProcessor executable and its
    DLL files to the main FFTProcessor folder after compilation. It took 
    me longer to write this code than it'd ever take to just move the
    files manually, but here we are anyways. 
    """

    # Determine the path to the FFTProcessor publish folder
    current_file = Path(__file__).resolve()
    compiled_path = current_file.parent / "bin/Release/net10.0/win-x64/publish"

    # Get all the EXE and DLL files
    all_files = []
    for root, _, files in os.walk(compiled_path):
        root_path = Path(root)
        for file in files:
            if file.endswith('.exe') or file.endswith('.dll'):
                all_files.append(root_path / file)

    # Move each file to the proper destination folder
    destination_folder = current_file.parent
    for file in all_files:

        destination_path = destination_folder / file.name
        if destination_path.exists():
            destination_path.unlink()  # removes file
        shutil.move(file, destination_path)

        print(f'Moved {file}')

# Run the function
publish()
