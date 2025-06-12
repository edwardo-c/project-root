import pandas as pd
from pos_xref.process.fuzzy_matching import FuzzyMatcher

''' 
test matching logic
'''

def test_fuzzy_matcher():
    '''
    should output 9 rows after matching sequence
    3 self matches because of the 3 unique names
    6 fuzzy matches because each entry matches the other two
    '''
    
    direct_data = {'acct_num':['AMZ135664'], 
              'customer_name': ['AMAZON DIRECT']}
    direct_df = pd.DataFrame(direct_data)

    foreign_data = {'acct_num':[None, None], 
                    'customer_name':['AMAZON LLC', 'AMAZON DC']}
    foreign_df = pd.DataFrame(foreign_data)
    
    matcher = FuzzyMatcher(direct_df, foreign_df, match_col='customer_name')
    matcher.run()
    
    # check column existence
    assert 'fuzzy_matches' in matcher.df_to_match.columns
    
    # check for nulls
    assert all(pd.notna(matcher.df_to_match['fuzzy_matches']))

    # count strings in fuzzy_matches
    assert list(matcher.df_to_match['fuzzy_matches'])

    # count number of fuzzy matches
    '''must be sensative enough to catch all matches for the test frame'''
    matcher.df_to_match['count_helper'] = matcher.df_to_match['fuzzy_matches'].apply(len)
    assert pd.Series.sum(matcher.df_to_match['count_helper']) == 9