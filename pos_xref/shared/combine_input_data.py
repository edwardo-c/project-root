import pandas as pd
import pos_xref.shared.direct_config as dc
import pos_xref.shared.pos_config as pc
import pos_xref.shared.utils as u
import utils.utils_io as uio

STANDARDIZED_COLUMNS = ['acct_num', 'customer_name', 'acct_group', 'bill_to_zip', 'bill_to_state']

def return_input_data(test_env:bool):
    
    files_info = [dc.DirectCustomersFileInfo(test_env), pc.POSCustomersFileInfo(2024,test_env)]
    output_df = pd.DataFrame()

    for info in files_info:
        df = _standardize_dataframe(info)
        output_df = pd.concat([df, output_df])
    
    return output_df

def _standardize_dataframe(info) -> pd.DataFrame:

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

    # convert remaining columns to string type data types
    df = df.astype({st_col:str for st_col in df.columns})

    df = df.drop_duplicates()

    # delete safe version
    uio.del_safe_path(safe_path_info)

    return df