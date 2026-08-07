# Christopher Esther, 7/17/2026
from pathlib import Path

def windows_long_path(path):
    path = str(Path(path))

    if len(path) >= 260 and not path.startswith('\\\\?\\'):
        path = '\\\\?\\' + path

    return Path(path)
