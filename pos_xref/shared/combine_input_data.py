import pandas as pd
from pos_xref.shared.pos_config import get_raw_pos_customers
from pos_xref.shared.direct_config import capture_direct_customers_df

def return_input_data(test_env:bool):
    direct_customers_df = capture_direct_customers_df(test_env=test_env)
    pos_xref_df = get_raw_pos_customers(year=2025, test_env=test_env)
    return pd.concat([direct_customers_df, pos_xref_df])