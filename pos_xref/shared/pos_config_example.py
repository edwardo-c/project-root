"""
pos_config_example.py

This is a template configuration for the POS Xref pipeline.
To use it:

1. Copy this file to pos_config.py
2. Edit the file paths and test mode as needed

This script supports a test mode that treats test files as if they are live data.
"""

import pandas as pd
import os
from typing import Dict

from utils.utils_io import gen_safe_excel_file

# Set this to True to use test files included in the repo
test_env = True

# Customize these paths for your environment
PROD_DIR = r"X:\Your\Real\Prod\Path"
TEST_DIR = r"./pos_xref/data/raw"  # Recommended test folder inside the repo
EXT = ".xlsx"
WS = "POS"

# The standardized columns returned from the sheet
STANDARDIZED_COLUMNS = ['sold_to_name', 'bill_to_zip', 'bill_to_state']

def get_raw_pos_customers(year: int, test_env: bool = True) -> pd.DataFrame:
    '''Returns standardized POS customer data for the specified year.'''
    info = IncentiveCompInfo(year, test_env)
    safe_path = gen_safe_excel_file(info.file_path())

    df = pd.read_excel(
        safe_path,
        sheet_name=info.ws,
        header=info.header_row()
    )

    column_header_map = _build_column_rename_map(info.column_headers())
    df = df[info.column_headers()].rename(columns=column_header_map).drop_duplicates()

    os.remove(safe_path)
    return df

def _build_column_rename_map(curr_cols) -> Dict:
    return {col: st_col for col, st_col in zip(curr_cols, STANDARDIZED_COLUMNS)}

class IncentiveCompInfo:
    '''Handles file path and column logic based on year and test mode.'''
    def __init__(self, year, test_env):
        if year not in range(2020, 2026):
            raise KeyError(f"{year} info not specified!")
        
        self.test_env = test_env
        self.base_dir = TEST_DIR if test_env else PROD_DIR
        self.year = year
        self.ws = WS

    def file_path(self):
        if self.year >= 2025:
            suffix = f"Incentive Comp - {self.year}"
        else:
            suffix = f"Incentive Comp - Bill To - Ship To - POS - {self.year}"
        return os.path.join(self.base_dir, suffix + EXT)

    def header_row(self) -> int:
        return 3 if self.year in range(2020, 2025) else 5

    def column_headers(self):
        if self.year <= 2021:
            return ['SOLD_TO_NAME', 'BILL_TO_CUST_ZIP', 'BILL_TO_CUST_STATE']
        else:
            return ['SoldToName', 'BillToCustomerZip', 'BillToCustomerState']
