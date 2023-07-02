"""Functions to include PowerShell scripts in Python code."""
from pathlib import Path

def get_file_as_str(file_path: Path) -> str:
    """Get a file as a string."""
    with open(file_path, "r") as file:
        file_str = file.read()
    return file_str

def get_all_files_in_dir_as_str(dir_path: Path, delimiter: str="\n") -> str:
    """Get all files in a directory as a string."""
    file_str = ""
    for file_path in dir_path.iterdir():
        file_str += get_file_as_str(file_path) + delimiter
    return file_str