from collections import defaultdict
import pandas as pd
from pos_xref.extract.file_reader import FileReader

class PreviousMatches():
    def __init__(self, test_env):
        self.df = pd.DataFrame()
        self.lookup = {}
        self.test_env = test_env
    def __str__(self):
        return f"Customers from Matches and Processed CSVs"
    
    def _get_data_frames(self):
        '''
        takes both data frames, consolidates and truncates only to pertinent columns
        '''
        matches = FileReader(self.test_env, 'matches')
        processed = FileReader(self.test_env, 'processed')
        matches.run()
        processed.run()

        self.df = pd.concat([matches.df, processed.df])
        self.df = self.df[['normalized_name', 'customer_name']]
        
    def _default_dict(self):
        '''builds a default dict to be used as a lookup structure for previous matches'''
        prev_matches = defaultdict(set)
        for norm, cust in zip(self.df['normalized_name'], self.df['customer_name']):
            prev_matches[norm].add(cust)

        self.lookup = prev_matches

    def run(self):
        self._get_data_frames()
        self._default_dict()
    