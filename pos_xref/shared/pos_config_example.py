'''
This script supports a test mode that treats test files as if they are live data.
'''
import pandas as pd
import os
from typing import Dict

from utils.utils_io import gen_safe_excel_file

STANDARDIZED_COLUMNS = ['customer_name', 'bill_to_zip', 'bill_to_state']

# Customize these paths for your environment
PROD_DIR = r"X:\Your\Real\Prod\Path"
TEST_DIR = r".\pos_xref\data\raw"  # Recommended test folder inside the repo
EXT = ".xlsx"
WS = "POS"

def get_raw_pos_customers(year: int, test_env:bool=True) -> pd.DataFrame:
    '''
    returns the distinc customers, bill to zip and bill to state columns from the raw data
    for a given year
    args:
        year: the year to specify which file to extract data from
        dir: the directory where the data lives (used for turning on and off the test switch)
    example input:
        get_raw_pos_customers(2024)
        {
            'sold_to_name':[AMAZON.COM, Apple HQ, Apple Inc, ], 
            'bill_to_zip', [98109, M5J 0A8, M5J 0A8], 
            'bill_to_state':[WA, ON, Ontario]
        }
    '''
    info = IncentiveCompInfo(year, test_env) # get file info by year, test flag for prod/dev switch
    
    safe_path = gen_safe_excel_file(info.file_path()) # create a safe file to read from
    
    df = pd.read_excel(
                    safe_path,
                    sheet_name=info.ws,
                    header=info.header_row()
                )
    
    ''' TODO: clean zip codes to five digits and ensure two letter states'''
    
    # get column mapping for renaming
    column_header_map = _build_column_rename_map(info.column_headers())
    
    # prepare truncated data frame (rename headers and drop duplicates inspecting all columns)
    df = df[info.column_headers()].rename(columns=column_header_map).drop_duplicates()

    # delete temp file after reading to delete sensative info
    os.remove(safe_path)
    
    return df

def _build_column_rename_map(curr_cols) -> Dict:
    '''
    build a mapping (dict) to rename columns
    args:
        curr_cols: name of the current columns. intended to be passed in as df.columns
    return: 
        dict mapped to the standardized column names
    example input:
        df = pd.DataFrame({'column_a':[1,2,3], 'column_b':[4,5,6], 'column_c':[7,8,9]})
        _build_column_rename_map(df.columns)
    example output:
        {'column_a': 'sold_to_name', 'column_b': 'bill_to_zip', 'column_c': 'bill_to_state'}    
    '''
    return {col:st_col for col, st_col in zip(curr_cols, STANDARDIZED_COLUMNS)}

class IncentiveCompInfo():
    ''' details info required to accurately file excel file, specific for the pos_xref'''
    def __init__(self, year, test_env):
        if year not in range (2020, 2026):
            raise KeyError(f"{year} info not specified! ")
        
        self.test_env = test_env
        
        if test_env:
            self.base_dir = TEST_DIR
        else:
            self.base_dir = PROD_DIR
        self.year = year
        self.ws = WS

    def file_path(self):
        if self.year >= 2025:
            suffix = f"Incentive Comp - {self.year}"
        else:
            suffix = f"Incentive Comp - Bill To - Ship To - POS - {self.year}"
        return os.path.join(self.base_dir, suffix + EXT)
    
    def header_row(self) -> int:
        '''returns the header row for pos incentive comp worksheets by year'''
        if self.year not in range(2020, 2026):
            raise ValueError (f"header_row for year {self.year} has not been defined")
        return 3 if self.year in range(2020, 2025) else 5
    
    def column_headers(self):
        '''used to import only pertinent columns'''
        '''TODO:
                check if these columns exist, raise error if not - 
                catching if column names have changed
        '''
        if self.year <= 2021:
            return ['SOLD_TO_NAME','BILL_TO_CUST_ZIP','BILL_TO_CUST_STATE']
        elif self.year >= 2022:
            return ['SoldToName','BillToCustomerZip','BillToCustomerState']