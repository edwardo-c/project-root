import pandas as pd
import pos_xref.shared.processed_matches_config 
import utils.utils_io as uio
from pos_xref.shared.processed_matches_config import ProcessedMatches


def get_previous_matches(test_env: bool) :

    info = ProcessedMatches(test_env=test_env)

    # create a safe (local copy) version, return the file path and data frame
    safe_path_info = uio.read_safe_csv_file(
        info.file_path(), 
        sheet_name=info.ws, 
        header_row=info.header_row()
    )

    # unpackage safe copy data frame
    df = safe_path_info['safe_data_frame']

    # delete safe version
    uio.del_safe_path(safe_path_info)

    return df



# create dictionary of normalized name, sold_to_name


# find new matches that have not been previously matched
    


# refresh processed_matches data frame with new matches