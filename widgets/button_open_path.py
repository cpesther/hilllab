# Christopher Esther, Hill Lab, 10/2/2025
import os
import subprocess
import platform
import ipywidgets as widgets
from IPython.display import display

def button_open_path(file_path, text=None, width=150, button_color='gray', 
                     text_color='white'):
    
    """
    Creates a clickable button in Jupyter Notebook that opens the path
    in the native file system.
    
    ARGUMENTS:
        file_path (string): Path to the file or folder to open.
    """

    # Determine the text to be displayed on the button
    if not text:
        button_text = f'Open: {file_path}'
    else:
        button_text = text

    # Create the button
    button = widgets.Button(description=button_text,
                            layout=widgets.Layout(width=f'{width}px'),
                            style={'button_color': button_color, 
                                   'font_weight': 'bold', 
                                   'color': text_color}
                            )
    button.on_click(lambda x: open_in_explorer(file_path))
    display(button)


def open_in_explorer(path):
    """Open the given file or folder in the system file explorer."""
    system = platform.system()
    if system == "Windows":
        if os.path.isdir(path):
            os.startfile(path)
        else:
            os.startfile(os.path.dirname(path))
    elif system == "Darwin":  # macOS
        subprocess.run(["open", "-R", path])
    else:  # Linux
        subprocess.run(["xdg-open", os.path.dirname(path)])
