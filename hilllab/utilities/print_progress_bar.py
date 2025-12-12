# Christopher Esther, Hill Lab, 8/15/2025
import sys
from datetime import datetime

def print_progress_bar(progress, total, title, multiple=1, bar_length=50):

    """
    Display a simple text progress bar in the console.

    ARGUMENTS:
        progress (int): Current progress count.
        total (int): Total count representing 100% completion.
        title (str): Label displayed before the progress bar.
        bar_length (int, optional): Width of the progress bar in characters.
    """

    # Only generate and print the progress bar if the progress value
    # is a multiple of the provided multiple value. This helps prevent
    # overloading print outputs by only refreshing the progress bar 
    # after every n iterations.
    if not progress % multiple:  # if no remainder (false) between progress and multiple

        # Calculate percent progress and the corresponding filled length
        percent = progress / total

        # This makes sure it fills completely
        if percent >= 98:
            filled_length = bar_length + 1
        else:
            filled_length = int(bar_length * percent)

        # Create the bar and print it
        time_value = str(datetime.now().time().replace(microsecond=0))

        bar = "█" * filled_length + "-" * (bar_length - filled_length)
        print(f"\r[{time_value}] {title} |{bar}| {percent:.0%} Complete", end="")

        sys.stdout.flush()  # clear the print outputs to avoid stacking
