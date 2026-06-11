# Christopher Esther, 2/21/2026
import subprocess
import platform

def clear_terminal():
    command = 'cls' if platform.system() == 'Windows' else 'clear'
    subprocess.run(command, shell=True)
    