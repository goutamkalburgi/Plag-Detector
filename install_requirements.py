"""
Installation Script for Project Dependencies

This script automates the installation process of the required packages for the project.
By executing this script, you can ensure all dependencies listed in `requirements.txt` are installed.

Usage:
    Run the script using your Python3 interpreter:
    $ python3 <filename>.py

Make sure `requirements.txt` is in the same directory as this script.

Note: Ensure you have appropriate permissions to install packages (you might need sudo/administrator rights).
"""

import subprocess
import sys

def install_requirements():
    """Install packages from requirements.txt."""
    try:
        # Check if pip is available
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)

        # Use pip to install the packages
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("All required packages are installed successfully!")
        
    except subprocess.CalledProcessError:
        print("Error during the installation of packages. Make sure you have pip installed and try again.")

if __name__ == '__main__':
    install_requirements()
