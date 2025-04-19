import pandas as pd
import shutil
import tempfile
import os

def gen_safe_excel_file(orig_file_path: str) -> str:
    '''
    Makes a temporary copy of the Excel file and reads from that instead.
    
    Args:
        file_path (str): Original Excel file path.
    Returns:
        file path of temp file to read from
    '''
    try:
        # create a temporary file path
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, os.path.basename(orig_file_path))

        # copy original file to temp
        shutil.copy2(orig_file_path, temp_path)

        return temp_path
    except Exception as e:
        raise RuntimeError(f"Failed to read Excel file safely: {e}")
