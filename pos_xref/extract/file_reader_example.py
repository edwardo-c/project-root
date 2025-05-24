import os
import pandas as pd
from pos_xref.utils.df_utils import column_rename_map
import pos_xref.transformations.normalize_data as nd
from utils import utils_io as uio


def test_file_details(ftype: str) -> dict:
    '''
    return all pertinent info for the files in the test system
    sheet_name and header row not required for csv file types
    
    for repo, point these file paths at:
        direct: .\pos_xref\data\raw\direct_customers_export.xlsx
        pos_sales: .\pos_xref\data\raw\Incentive Comp - 2025.xlsx
        matches: .\pos_xref\data\output\matches.csv
        processed: .\pos_xref\data\processed\processed_matches.csv
    '''

    d = {
        'direct' : {'file_path': r"C:\test\path\pos_xref\data\raw\direct_customers_export.xlsx",
                    'sheet_name': 'Data',
                    'header_row': 0,
                    'columns': ['Customer ID', 'Customer Name', 'State', 'Postal Code', 'Account Group']},
        'pos_sales': {'file_path': r"C:\test\path\pos_xref\data\raw\Incentive Comp - 2025.xlsx", 
                    'sheet_name': 'POS',
                    'header_row': 5,
                    'columns':['SoldToName', 'BillToCustomerZip', 'BillToCustomerState']}, 
        'matches' : {'file_path': r"C:\test\path\pos_xref\data\output\matches.csv"},
        'processed' : {'file_path': r"C:\test\path\pos_xref\data\processed\processed_matches.csv"}
    }
    return d[ftype]

def prod_file_details(ftype: str) -> dict:
    '''
    FOR REPO:
    PROD_FILE_DETAILS ARE NOT USED IN THE GITHUB REPO
    This is a place holder for the real internal system. 
    The files processed exist on a shared network drive.
    
    Original comments:
    return all file paths for the prod system
    sheet_name and header row not required for csv file types
    '''
    d = {
        'direct' : {'file_path': r"H:\my\prod\path\direct_customers_export.xlsx",
                    'sheet_name': 'Data',
                    'header_row': 0},
        'pos_sales': {'file_path': r"H:\my\prod\path\\Incentive Comp - 2025.xlsx", 
                    'sheet_name': 'POS',
                    'header_row': 5}, 
        'matches' : {'file_path': r"H:\my\prod\path\approved_matches.csv"},
        'processed' : {'file_path': r"H:\my\prod\path\processed_matches.csv"}
    }

    return d[ftype]

class FileReader():
    def __init__(self, test_env, ftype):
        self.test_env = test_env
        self.ftype = ftype
        self.file_details = {}
        self.df = None
    def __str__(self):
        return "FileReader for test_env" if self.test_env else "FileReader for prod"
    
    def file_path_details(self):
        '''procedural method to return dictionary containing specified file's info'''
        if self.test_env:
            self.file_details = test_file_details(self.ftype)
        else:
            self.file_details = prod_file_details(self.ftype)
    def load_file_info(self):
        self.file_path = self.file_details.get('file_path')
        self.sheet_name = self.file_details.get('sheet_name', None)
        self.header_row = self.file_details.get('header_row', 0)
        self.columns = self.file_details.get('columns', 0)
        self.file_ext = os.path.splitext(os.path.basename(self.file_path))[1]
    
    def read_df(self) -> pd.DataFrame:
        info = uio.read_safe_excel_file(orig_file_path=self.file_path,
                                        sheet_name=self.sheet_name,
                                        header_row=self.header_row,
                                        ftype=self.file_ext)
        
        self.df = info['safe_data_frame'] # unpackage data frame from info
        # truncate to pertinent columns only
        uio.del_safe_path(info)

    def _normalize_df(self):
        '''
        direct and pos_sales requiring standardization of column names
        '''
        # standardize column names and truncate only to standardized columns
        if self.ftype == "direct":
            STANDARDIZED_COLUMNS = ['acct_num', 'customer_name', 'bill_to_state', 'bill_to_postal_code', 'acct_group']
        elif self.ftype == 'pos_sales':
            STANDARDIZED_COLUMNS = ['customer_name', 'bill_to_postal_code', 'bill_to_state']

        self.df = self.df.rename(columns=column_rename_map(self.columns, STANDARDIZED_COLUMNS))[STANDARDIZED_COLUMNS] 

        self.df = self.df.drop_duplicates('customer_name')

        if 'normalized_name' in self.df.columns:
            return # early exit if normalized name already exists. 
                   # Processed and match files will have normalized name
        
        # add normalized names; use acct group name if it has one
        if not 'acct_group' in self.df.columns:
            self.df['normalized_name'] = self.df['customer_name'].apply(lambda row: nd.normalize_name(row) if pd.notna(row) else row)
        else: 
            self.df['normalized_name'] = self.df.apply(
                lambda row: nd.normalize_name(row['customer_name']) if pd.isnull(row['acct_group'])
                            else nd.normalize_name(row['acct_group']),
                axis=1
                )
        
        # clean postal code
        self.df['bill_to_postal_code'] = self.df['bill_to_postal_code'].apply(nd.normalize_postal_code)

    def run(self):
        self.file_path_details()
        self.load_file_info()
        self.read_df()
        if (self.ftype == 'pos_sales') or (self.ftype == 'direct'):
            ''' matches and processed are created pos normalization of raw data; 
                normalization not needed'''
            self._normalize_df()


