'''
shared utility functions for consolidating input data
'''
from typing import Dict
import pandas as pd

def _build_column_rename_map(curr_cols, st_cols) -> Dict:
    '''build a dict to rename current columns to standardized columns (st_cols)
    '''
    return {col: st_col for col, st_col in zip(curr_cols, st_cols)}

def _confirm_headers(cols, expected_columns) ->bool:
    for header in expected_columns:
        if not header in cols:
            raise KeyError(f"Expected header {header} not found")
    return True

def _convert_columns_dtypes(df: pd.DataFrame, cols_to_update: Dict) -> pd.DataFrame:
    '''
    Loop through data frame converting columns to specified data type
    '''
    df = df.astype(cols_to_update)

    return df