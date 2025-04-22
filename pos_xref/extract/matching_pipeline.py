import pandas as pd
import pos_xref.shared.processed_matches_config 
import utils.utils_io as uio
from pos_xref.shared.processed_matches_config import ProcessedMatches


def get_processed_matches(test_env: bool) :

    info = ProcessedMatches(test_env=test_env)

    # create a safe (local copy) version, return the file path and data frame
    safe_path_info = uio.read_safe_excel_file(orig_file_path=info.file_path(), ftype='csv')

    # unpackage safe copy data frame
    df = safe_path_info['safe_data_frame']

    lookup_structure = _lookup_structure(df)
    print(lookup_structure)

    # delete safe version
    uio.del_safe_path(safe_path_info)

    return lookup_structure

def _lookup_structure(df):
    # create dictionary of normalized name, sold_to_name
    d = {}
    for n_name, o_name  in zip(df['normalized_name'], df['customer_name']):
        if not n_name in d.keys():
            d[n_name] = o_name
    return d



# find new matches that have not been previously matched
    


# refresh processed_matches data frame with new matches