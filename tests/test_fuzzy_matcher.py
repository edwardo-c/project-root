import pytest
import pandas as pd
from pos_xref.process.fuzzy_matching import FuzzyMatcher

def test_fuzzy_matcher(direct_df, foreign_df):
    '''Tests for FuzzyMatcher'''

    matcher = FuzzyMatcher(direct_df, foreign_df, match_col='customer_name')
    matcher.run()

    # Assert 'fuzzy_matches' column exists
    assert 'fuzzy_matches' in matcher.df_to_match.columns

    # Assert no nulls in fuzzy_matches
    assert all(pd.notna(matcher.df_to_match['fuzzy_matches']))

    # Total match objects expected = 3 matches per row * 3 rows = 9
    assert matcher.df_to_match['fuzzy_matches'].apply(len).sum() == 9