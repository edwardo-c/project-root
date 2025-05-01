import pandas as pd
from collections import defaultdict
from typing import Dict
from rapidfuzz import process
import utils.utils_io as uio
from pos_xref.shared.processed_matches_config import ProcessedMatches
from pos_xref.shared.matches_config import Matches

def fill_output_file(test_env: bool):
    '''
    capture the current processed data fill with new fuzzy matches and similarity score
    exclude matches already made and self matches
    '''


    # get existing output data from files and lookup structure
    processed_data_package = get_processed_matches(test_env=test_env)
    output_file, processed_matches = processed_data_package

    # fill output file with new matches
    output_file['fuzzy_results'] = output_file['customer_name'].apply()
    df = pd.DataFrame()
    df.apply()

    pass


def get_processed_matches(test_env: bool) -> Dict[str, list]:
    '''
    returns a dict(list) to test if a fuzzy match has been matched before
    processed matches: confirmed matches, mismatch, or unreviewed
    example:
        {
            amazon: [AMAZON, amazon inc, Amazon.com] (matches)
            apple: [Appleson, Applewood] (mismatches)
            netflix: [netflix branch ca, netfloxan] (match and mismatch)
        }
    the type of match is irrelavent, only checking if previously matched
    '''
    # concat data frames of matches and processed
    previously_reviewed_info = [ProcessedMatches(test_env=test_env), Matches(test_env=test_env)]
    previously_matched_df = pd.DataFrame()

    # get pd, concat to final df, delete safe file
    for info in previously_reviewed_info:
        # create a safe (local copy) version, return the file path and data frame
        safe_path_info = uio.read_safe_excel_file(orig_file_path=info.file_path(), ftype='csv')
        df = safe_path_info['safe_data_frame'] # extract data
        uio.del_safe_path(safe_path_info) # delete safe version
        previously_matched_df = pd.concat([df, previously_matched_df]) # concat to final df

    # convert data frame into look up structure
    processed_matches = defaultdict(list)
    for norm, original in zip(previously_matched_df['normalized_name'], previously_matched_df['customer_name']):
        processed_matches[norm].append(original)

    return [df, processed_matches]


def new_matches(norm_name, all_norm_names, name_mapping: Dict, previous_matches):
    '''
    Return fuzzy matches for a given customer, excluding matches previously completed
    args:
        all_customers: the customers to query against

    Query against normalized names; return customer_name
    exclude self matches
    exclude previously matched
    '''
    raw_matches = process.extract(query=norm_name, choices=all_norm_names, score_cutoff=88, limit=20)
    new_matches = []
    # remove previous matches
    for match in raw_matches:
        if (norm_name, match[0]) not in previous_matches:
            '''append original, non-normalized name to return matches'''
            new_matches.append(name_mapping[match[0]])

    return new_matches