import pandas as pd
import numpy as np
import pos_xref.shared.direct_config as dc
import pos_xref.transformations.normalize_data as nd

STANDARDIZED_COLUMNS = ['acct_num', 'customer_name', 'acct_group', 'bill_to_state', 'bill_to_postal_code']

def return_input_data(test_env:bool):
    
    direct = dc.FileReader(test_env, 'direct')
    direct.run()

    pos = dc.FileReader(test_env, 'pos_sales')
    pos.run()
    
    data_frames = [direct.df, pos.df]
    output_df = pd.concat([direct.df, pos.df])

    return output_df

def _normalize_data(df:pd.DataFrame) -> pd.DataFrame:
    '''Vectorized normalization of customer names, postal codes, and states'''

    # convert columns to string type data types and dedupe
    df = df.astype({col:str for col in df.columns}).drop_duplicates()

    # TODO: normalize account group, if null fall back to normalize customer name
    # still not working, need to understand this better
    df['normalized_name'] = df.apply(
        lambda row: nd.normalize_name(row['acct_group']) if pd.notna(row['acct_group']) and row['acct_group'] != ""
        else nd.normalize_name(row['customer_name']),
        axis=1
        )

    # normalize postal codes
    df['bill_to_postal_code'] = df['bill_to_postal_code'].apply(nd.normalize_postal_code)

    # TODO: Normalize states
    df['bill_to_state'] = df['bill_to_state'].apply(str.upper)

    print(df)

    return df