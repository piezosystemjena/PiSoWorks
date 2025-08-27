"""
generate_version.py

This script generates a VERSION file containing the current application version.
The version is determined dynamically using Poetry (with poetry-dynamic-versioning
enabled), so it reflects the latest Git tag, commit count, or other rules defined
by the plugin.

Usage:
    python generate_version.py

Output:
    Creates/overwrites a file named 'VERSION' with the current version string.

Example VERSION contents:
    1.0.4           # exact tag
    1.0.5.dev2       # two commits after the 1.0.4 tag

Requirements:
    - Python 3.x
    - Poetry installed and in PATH
    - poetry-dynamic-versioning plugin enabled
"""

import subprocess
from pathlib import Path

VERSION_FILE = "VERSION"

def get_version() -> str:
    """
    Retrieve the current application version from Poetry.

    Returns:
        str: The version string, e.g., "1.0.4" or "1.0.5.dev2".
    
    Falls back to "0.0.0" if Poetry is not available or an error occurs.
    """
    try:
        # Call Poetry to get the current version
        version = subprocess.check_output(
            ["poetry", "version", "-s"],  # -s returns only the version string
            stderr=subprocess.STDOUT
        ).decode().strip()
        return version
    except Exception as e:
        print(f"Warning: Could not determine version via Poetry: {e}")
        return "0.0.0"

def write_version_file(version: str, filepath: str = VERSION_FILE):
    """
    Write the version string to the VERSION file.

    Args:
        version (str): The version string to write.
        filepath (str): The path of the file to write to (default: 'VERSION').
    """
    path = Path(filepath)
    path.write_text(version)
    print(f"Wrote version '{version}' to {filepath}")



if __name__ == "__main__":
    current_version = get_version()
    write_version_file(current_version)
