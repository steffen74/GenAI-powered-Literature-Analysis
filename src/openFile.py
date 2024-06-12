import os
import subprocess
def open_file(file_path):
    """
    Opens a file using the default program associated with the file type on Windows.

    Parameters:
    file_path (str): The path to the file to be opened.
    """
    try:
        if os.path.exists(file_path):
            # Using start command to open the file with the default application
            subprocess.run(['start', '', file_path], shell=True, check=True)
            print(f"File {file_path} opened successfully.")
        else:
            print(f"File {file_path} does not exist.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to open file {file_path}. Error: {e}")