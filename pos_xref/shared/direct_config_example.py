'''
Example for public repo
For test, ensure test_mode = True in runner function, intended to be passed from main.py in pos_xref 
'''
import pandas as pd
from typing import Dict
from os import remove
from pos_xref.shared import utils as u
from utils.utils_io import gen_safe_excel_file

DIRECT_CUST_FILE_PATH = r"C:\My\Shared\Excel\File\direct_customers_export.xlsx" # prod data
TEST_FILE_PATH = r".\pos_xref\data\raw\direct_customers_export.xlsx" # Recommended test folder inside the repo
STANDARDIZED_COLUMNS = ['acct_num', 'customer_name', 'acct_group', 'bill_to_zip', 'bill_to_state']

## runner function: 
def capture_direct_customers_df(test_env:bool=True):
    '''
        return a df containing only pertinant columns from the direct customers file
        with standardized column names: [
            'acct_num', 'customer_name', 'acct_group', 'bill_to_zip', 'bill_to_state'
            ]
    '''
    # read file info
    info = DirectCustomersFileInfo(test_env)
    
    # create a safe (local copy) version to read from
    local_copy = gen_safe_excel_file(info.file_path())

    # read safe copy
    df = pd.read_excel(local_copy, sheet_name=info.WS)

    df = _standardized_df(df, info)

    # delete safe version
    remove(local_copy)

    return df

## helper functions
def _standardized_df(df:pd.DataFrame, info) -> pd.DataFrame:
    '''
    Takes original df from pd.read and standardizes it.
        - rename columns
        - keep only specified columns
    args:
        df: the data frame to be manipulated
    info:
        custom class holding expected data frame info

    '''
    # confirm expected headers existence
    u._confirm_headers(df.columns, info.EXPECTED_COLUMNS)

    # truncate data frame to pertinent columns only
    df = df[info.EXPECTED_COLUMNS]

    # rename columns to spec
    df = df.rename(columns=u._build_column_rename_map(df.columns, STANDARDIZED_COLUMNS))

    return df


## class contianing file info to capture df
class DirectCustomersFileInfo:
    def __init__(self, test_env):
        self.test_env = test_env

    def file_path(self):
        if self.test_env:
            return TEST_FILE_PATH
        return DIRECT_CUST_FILE_PATH

    WS = "Data" 
    EXPECTED_COLUMNS = ['Customer ID', 'Customer Name', 'Account Group', 'State', 'Postal Code']  
