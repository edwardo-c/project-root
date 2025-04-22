'''
This script supports a test mode that treats test files as if they are live data.
'''
import pandas as pd
import os

STANDARDIZED_COLUMNS = ['customer_name', 'bill_to_postal_code', 'bill_to_state']
PROD_DIR = r"X:\Your\Real\Prod\Path"
TEST_DIR = r".\pos_xref\data\raw"  # Recommended test folder inside the repo
EXT = ".xlsx"

def rename_columns(df:pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={col:st_col 
                            for col, st_col in 
                            zip(df.columns, STANDARDIZED_COLUMNS)
                            }
                        )
    return df

class POSCustomersFileInfo():
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
        self.ws = "POS"
        self.cust_type = "POS"

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

    def expected_columns(self):
        '''used to import only pertinent columns'''
        '''TODO:
                check if these columns exist, raise error if not - 
                catching if column names have changed
        '''
        if self.year <= 2021:
            return ['SOLD_TO_NAME','BILL_TO_CUST_ZIP','BILL_TO_CUST_STATE']
        elif self.year >= 2022:
            return ['SoldToName','BillToCustomerZip','BillToCustomerState']     