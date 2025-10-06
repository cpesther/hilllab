# Christopher Esther, Hill Lab, 10/06/2025
from datetime import datetime

def pretty_timestamp():
    dt = datetime.now()
    formatted = dt.strftime("%B %d, %Y at %I:%M %p")
    return formatted
