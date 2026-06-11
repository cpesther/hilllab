# Christopher Esther, 2/21/2026
from datetime import datetime

def format_timestamp(timestamp):
    ts = datetime.fromtimestamp(timestamp)
    formatted_date = ts.strftime('%m/%d/%Y')
    formatted_time = ts.strftime('%H:%M:%S')
    return formatted_date, formatted_time
