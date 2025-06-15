'''
takes two data frame inputs and fuzzy_matches all names.
outputs a cross reference between all match options
includes match score
'''

import pandas as pd
from rapidfuzz import process

class FuzzyMatcher():
    '''
    consolidate data frames and run fuzzy match on specified column
    '''
    def __init__(self, *sep_dfs, match_col='normalized_name', score_cutoff=70):
        if not sep_dfs:
            raise ValueError("At least one DataFrame must be provided.")

        if not all(isinstance(df, pd.DataFrame) for df in sep_dfs):
            raise TypeError("All inputs must be pandas DataFrames.")

        self.sep_dfs = list(sep_dfs)
        self.match_col = match_col
        self.score_cutoff = score_cutoff
        self.fuzzy_match_count: int = 0
    
    def __repr__(self):
        return f"FuzzyMatcher(sep_dfs, match_col={self.match_col}, score_cutoff={self.score_cutoff})"

    def __str__(self):
        return f"FuzzyMatcher; Consolidate dfs and run fuzzy_match on {self.match_col}"
    
    def __len__(self) -> int:
        if not hasattr(self, 'df_to_match') or 'fuzzy_matches' not in self.df_to_match.columns: 
            return 0
        return len(self.df_to_match)

    def _concat_dfs(self):
        self.df_to_match = pd.concat(self.sep_dfs, ignore_index=True)

    def _fuzzy_matching(self):
        '''
        return matching results in seperate column
        '''
        choices = set(self.df_to_match[self.match_col])

        self.df_to_match['fuzzy_matches'] = self.df_to_match[self.match_col].apply(
            lambda x: 
            process.extract(x, choices=choices, score_cutoff=self.score_cutoff)
        )
    
    def _count_fuzzy_matches(self):
        self.fuzzy_match_count = self.df_to_match['fuzzy_matches'].apply(len).sum()
        
    def run(self):
        self._concat_dfs()
        self._fuzzy_matching()
        self._count_fuzzy_matches()


