# Christopher Esther, 08/15/2025
def format_duration(seconds):

    """
    Takes a duration in seconds and formats it into the most logical
    units of time which are returned as a string.
    """

    if seconds < 0:
        raise ValueError("Duration cannot be negative.")

    units = [
        ('d', 86400),
        ('hr', 3600),
        ('m', 60),
        ('s', 1)
    ]

    parts = []
    for name, count in units:
        value, seconds = divmod(seconds, count)
        if value:
            parts.append(f"{int(value)} {name}")

    return ' '.join(parts) if parts else "0 s"
