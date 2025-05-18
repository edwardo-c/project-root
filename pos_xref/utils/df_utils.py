'''
shared utility functions for consolidating input data
'''
from typing import Dict

def column_rename_map(curr_cols, st_cols) -> Dict:
    '''build a dict to rename current columns to standardized columns (st_cols)
    '''
    return {col: st_col for col, st_col in zip(curr_cols, st_cols)}

def _confirm_headers(cols, expected_columns) ->bool:
    for header in expected_columns:
        if not header in cols:
            raise KeyError(f"Expected header {header} not found")
    return True