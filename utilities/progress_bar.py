# Christopher Esther, 08/15/2025
import sys
from datetime import datetime

def progress_bar(progress, total, title, bar_length=50):

    """
    Display a simple text progress bar in the console.

    ARGUMENTS:
        progress (int): Current progress count.
        total (int): Total count representing 100% completion.
        title (str): Label displayed before the progress bar.
        bar_length (int, optional): Width of the progress bar in characters.
    """

    # Calculate percent progress and the corresponding filled length
    percent = progress / total
    filled_length = int(bar_length * percent)

    # Create the bar and print it
    time_value = str(datetime.now().time().replace(microsecond=0))

    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    print(f"\r[{time_value}] {title} |{bar}| {percent:.0%} Complete", end="")

    sys.stdout.flush()  # clear the print outputs to avoid stacking
