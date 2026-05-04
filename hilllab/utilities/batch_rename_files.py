# Christopher Esther, Hill Lab, 5/1/2026
import os

def batch_rename_files(folder_path, old, new):

    """
    Renames all files in a folder by replacing the old string with the
    new string.

    ARGUMENTS:
        folder_path (string): the path to the folder with the files to be
            renamed.
        old (string): the old string in the file name to be replaced
        new (string): the new string used to replace the old string
    """

    # Print the new changed names for verification
    print('Please verify the new names for the files:')
    for item in os.listdir(folder_path):
        print(item.replace(old, new))

    # Ask for verification
    verificiation = input('Are these new names correct? y/[n]: ')

    # If verified, perform renaming
    if verificiation.upper() == 'Y':
        for item in os.listdir(folder_path):
            full_path = os.path.join(folder_path, item)
            new_path = os.path.join(folder_path, item.replace(old, new))
            os.rename(full_path, new_path)

        print('Renaming complete!')
