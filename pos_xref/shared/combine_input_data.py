import pandas as pd
import pos_xref.shared.direct_config as dc
import pos_xref.shared.pos_config as pc
import pos_xref.shared.utils as u
import utils.utils_io as uio
import pos_xref.transformations.normalize_data as nd

STANDARDIZED_COLUMNS = ['acct_num', 'customer_name', 'acct_group', 'bill_to_state', 'bill_to_postal_code']

def return_input_data(test_env:bool):
    
    files_info = [dc.DirectCustomersFileInfo(test_env), pc.POSCustomersFileInfo(2024,test_env)]
    output_df = pd.DataFrame()

    for info in files_info:
        df = _extract_dataframe(info)
        output_df = pd.concat([df, output_df])
    
    output_df = _normalize_data(output_df)

    return output_df

def _normalize_data(df:pd.DataFrame) -> pd.DataFrame:
    '''Vertorized application of normalization functions'''

    # convert columns to string type data types and dedupe
    df = df.astype({col:str for col in df.columns}).drop_duplicates()

    df['normalized_name'] = df['customer_name'].apply(nd.normalize_name)

    # normalize postal codes
    df['bill_to_postal_code'] = df['bill_to_postal_code'].apply(nd.normalize_postal_code)

    # TODO: Normalize states
    df['bill_to_state'] = df['bill_to_state'].apply(str.upper)

    return df

def _extract_dataframe(info) -> pd.DataFrame:

    # create a safe (local copy) version, return the file path and data frame
    safe_path_info = uio.read_safe_excel_file(
        info.file_path(), 
        sheet_name=info.ws, 
        header_row=info.header_row()
    )

    # unpackage safe copy data frame
    df = safe_path_info['safe_data_frame']

    # confirm expected headers existence
    u._confirm_headers(df.columns, info.expected_columns())

    # truncate data frame to pertinent columns only
    df = df[info.expected_columns()]

    # customer type specific data frame modifications; 
    # for now only the renaming of columns is different

    if info.cust_type == "Direct":
        df = df.rename(columns=u._column_rename_map(df.columns, STANDARDIZED_COLUMNS))
    elif info.cust_type == "POS":
        df = pc.rename_columns(df)
    else:
        raise KeyError(f"unspecified customer type")

    # delete safe version
    uio.del_safe_path(safe_path_info)

    return df