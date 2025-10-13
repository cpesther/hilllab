from setuptools import setup, find_packages
from pathlib import Path

# Read version from file
__version__ = "1.1.1.251013"

# Read requirements
req_file = Path(__file__).parent / "requirements.txt"
install_requires = req_file.read_text().splitlines()

setup(
    name="hilllab",
    version=__version__,
    packages=find_packages(),
    install_requires=install_requires,
    python_requires=">=3.10",
    author="Christopher Esther",
    description="Code used in the David Hill Lab in the Marsico Lung Institute at UNC-CH",
    url="https://github.com/cpesther/hilllab"
)
