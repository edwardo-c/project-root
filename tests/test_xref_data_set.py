import pytest
import re
import pandas as pd
from pos_xref.extract.file_reader import XRefDataSet

# def column_checker(col_name: str, df: pd.DataFrame) -> bool:
#     return bool(col_name in df.columns)

def test_remove_special_characters():
   assert XRefDataSet._remove_special_characters('$^&!APPLE 8+') == 'APPLE 8'

def test_remove_suffixes():
    assert XRefDataSet._remove_suffixes('APPLE ORG CO') == 'APPLE'
    # expected to leave behind two spaces

def test_normalize_name():
    assert XRefDataSet._normalize_name('$^&!APPLE+ INC') == 'apple'
        