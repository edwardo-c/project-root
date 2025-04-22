import pandas as pd
import shutil
import tempfile
import os
from typing import Dict

def read_safe_excel_file(orig_file_path: str, sheet_name: str = '', header_row: int = 0, ftype='xlsx') -> Dict:
    '''
    Makes a temporary copy of the Excel file and reads from that instead.
    
    Args:
        file_path (str): Original Excel file path.
        sheet_name (str): name of the worksheet to read
        header_row (int): row index for headers
    Returns:
        Dict containing file path to temp file and dataframe captured from file
    '''
    try:
        # create a temporary file path
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, os.path.basename(orig_file_path))

        # copy original file to temp
        shutil.copy2(orig_file_path, temp_path)

        # read temporary file data frame
        if ftype == 'xlsx':
            if not (sheet_name) and (not header_row):
                raise KeyError(f"missing sheet name or header row for {ftype} file")
            df = pd.read_excel(temp_path, sheet_name=sheet_name, header=header_row)
        elif ftype == 'csv':
            df = pd.read_csv(temp_path)
        else:
            raise KeyError(f"{ftype} is an invalid file type")

        return {'temp_file_path': temp_path, 'safe_data_frame': df}
    
    except Exception as e:
        raise RuntimeError(f"Failed to read Excel file safely: {e}")


def del_safe_path(safe_path_info: Dict):
    os.remove(safe_path_info['temp_file_path'])