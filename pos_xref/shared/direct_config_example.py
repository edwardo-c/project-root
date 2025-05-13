import os
from utils import utils_io as uio
import pandas as pd


def test_file_details(ftype: str) -> dict:
    '''
    return all file paths for the test system
    sheet_name and header row not required for csv file types
    '''
    
    '''
    for repo, point these file paths at:
        direct: .\pos_xref\data\raw\direct_customers_export.xlsx
        pos_sales: .\pos_xref\data\raw\Incentive Comp - 2025.xlsx
        matches: .\pos_xref\data\output\matches.csv
        processed: .\pos_xref\data\processed\processed_matches.csv
    '''

    d = {
        'direct' : {'file_path': r"test\path\pos_xref\data\raw\direct_customers_export.xlsx",
                    'sheet_name': 'Data',
                    'header_row': 0},
        'pos_sales': {'file_path': r"C:\test\path\pos_xref\data\raw\Incentive Comp - 2025.xlsx", 
                    'sheet_name': 'POS',
                    'header_row': 5}, 
        'matches' : {'file_path': r"C:\test\path\pos_xref\data\output\matches.csv"},
        'processed' : {'file_path': r"C:\test\path\pos_xref\data\processed\processed_matches.csv"}
    }
    return d[ftype]

def prod_file_details(ftype: str) -> dict:
    '''
    return all file paths for the test system
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
        # TODO: update needed for refactor
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
        self.file_ext = os.path.splitext(os.path.basename(self.file_path))[1]
    
    def read_df(self) -> pd.DataFrame:
        info = uio.read_safe_excel_file(orig_file_path=self.file_path,
                                        sheet_name=self.sheet_name,
                                        header_row=self.header_row,
                                        ftype=self.file_ext)
        self.df = info['safe_data_frame']
        uio.del_safe_path(info)

    def run(self):
        self.file_path_details()
        self.load_file_info()
        self.read_df()


        


