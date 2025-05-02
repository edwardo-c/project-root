'''
fill matches.csv with "self-matches", as in customer name: normalized name pairs
Removing these eliminates the need for the user to confirm these relavent but easily paired matches
'''

from collections import defaultdict
from pos_xref.shared.matches_config import Matches
from pos_xref.extract.customer_class import Customer
import utils.utils_io as uio
import pandas as pd

temp_df = pd.DataFrame()
temp_df


def update_self_matches(test_env: bool, all_custs_df):
    
    # get file info to capture current matches
    info = Matches(test_env=test_env)
    matches_info = uio.read_safe_excel_file(orig_file_path=info.file_path(), ftype=info.ext)
    matches_df = matches_info['safe_data_frame']
    
    # get current matches in a lookup structure to avoid duplicating in matches df
    matches_lookup = _matches_lookup(matches_df)

    # capture only new self matches
    new_self_matches = _identify_new_self_matches(all_custs_df, matches_lookup)

    # structure new self matches to concat with current matches.csv
    nsm_df = _convert_nsm_to_df(new_self_matches)

    # prepare matches.csv
    save_self_matches(nsm_df, matches_df)

    uio.del_safe_path(matches_info)

def save_self_matches(nsm_df, matches_df):

    matches_output = pd.concat([matches_df, nsm_df])

    print(matches_output) # currently not catching normalized name properly

    # TODO: save updates matches df

def _convert_nsm_to_df(new_self_matches) -> pd.DataFrame:
    data = [
        {
            'acct_num':nsm.acct_num,
            'normalized_name':nsm.norm,
            'customer_name':nsm.orig,
            'match_type':nsm.match_type
            }
        
        for nsm in new_self_matches
        ]
    
    return pd.DataFrame(data)

def _identify_new_self_matches(all_cust_df, matches_lookup):
    '''
    loop through all customers, check if they already exist,
    if not add their info to a customer class
    ''' 

    self_matches = []

    all_self_matches = zip(
                            all_cust_df['acct_num'],
                            all_cust_df['customer_name'],
                            all_cust_df['normalized_name'],
                            )

    for acct_num, orig, norm in all_self_matches:
        if not (norm, orig) in matches_lookup:
            self_matches.append(Customer(
                acct_num=acct_num, norm=norm, orig=orig, match_type="self-match")
                )

    return self_matches

def _matches_lookup(matches_df) -> list:
    '''
    Build the lookup structure for confirmed matches only
    '''
    # convert data frame into look up structure
    matches_lookup = defaultdict(list)
    for norm, original in zip(matches_df['normalized_name'], matches_df['customer_name']):
        matches_lookup[norm].append(original)

    return matches_lookup