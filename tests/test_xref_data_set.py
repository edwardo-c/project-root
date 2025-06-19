import pytest
import pandas as pd
from pos_xref.extract.file_reader import XRefDataSet, SUFFIXES

'''
Tests:
column names
normalized_name col was added
'''

def column_checker(col_name: str, df: pd.DataFrame) -> bool:
    return bool(col_name in df.columns)

def test_XRefDataSet():
    primary = XRefDataSet()
    foreign = XRefDataSet()

    data_sets = [primary, foreign]
    
    for data_set in data_sets():
        
        assert column_checker('normalized_name', data_set)

        # test removal of suffixes
        norm_names = ''.join(set(data_set['normalized_name']))
        assert all(suffix not in norm_names for suffix in SUFFIXES)
        
        # test lower case text
        assert norm_names.islower()

        # ensure transformations were made for each
        if data_set._acct_nums:
            assert column_checker('acct_nums', data_set)
            
        if data_set._state:
            assert column_checker('state', data_set)

        if data_set._postal:
            assert column_checker('postal', data_set)
        