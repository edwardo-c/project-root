import pandas as pd
from pos_xref.extract.file_reader import FileReader # base data
from pos_xref.extract.process_output import ProcessedOutput

test_env=False

def test_direct_base():
    base_direct = FileReader(test_env=test_env, ftype='direct')
    base_direct.run()
    df = base_direct.df
    assert "acct_num" in df.columns, "acct_num column is missing"
    assert df["acct_num"].notnull().all(), "acct_num has nulls"
    assert (df["acct_num"].astype(str).str.strip() != "").all(), "acct_num has blanks"

def test_processed_output():
    po = ProcessedOutput(test_env)
    po.run()
    df = po.fuzzy_matches_df
    assert "acct_num" in df.columns, "acct_num column is missing"
    assert df["acct_num"].notnull().all(), "acct_num has nulls"
    assert (df["acct_num"].astype(str).str.strip() != "").all(), "acct_num has blanks"