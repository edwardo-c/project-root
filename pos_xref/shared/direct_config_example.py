'''
Example for public repo
For test, ensure test_mode = True in runner function, intended to be passed from main.py in pos_xref 
'''
import pandas as pd
from typing import Dict

DIRECT_CUST_FILE_PATH = r"C:\My\Shared\Excel\File\direct_customers_export.xlsx" # prod data
TEST_FILE_PATH = r".\pos_xref\data\raw\direct_customers_export.xlsx" # Recommended test folder inside the repo

## class contianing file info to capture df
class DirectCustomersFileInfo:
    def __init__(self, test_env):
        self.test_env = test_env
        self.ws = "Data"
        self.cust_type = "Direct"

    def file_path(self):
        if self.test_env:
            return TEST_FILE_PATH
        return DIRECT_CUST_FILE_PATH

    def header_row(self):
        return 0
    
    def expected_columns(self): 
        return ['Customer ID', 'Customer Name', 
                'Account Group', 'State', 
                'Postal Code'
                ]  
