# Christopher Esther, Hill Lab, 7/13/2026
from pathlib import Path

ROOT_DIR = Path(r'J:\Hill Lab')
#ROOT_DIR = Path(r'J:\Hill Lab\Presentations & Papers\Presentations\8.8.17\Artificial Mucus\References')
DATABASE_PATH = ROOT_DIR / 'index.db'

# Scanning rules
scan_rules = {
    'default_interval': 86400,   # 1 day
    'minimum_interval': 600,     # 10 minutes
    'maximum_interval': 604800,  # 7 days
}