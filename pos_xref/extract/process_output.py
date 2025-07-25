from typing import Dict
from rapidfuzz import process
import pandas as pd
from pos_xref.extract.previous_matches import PreviousMatches
from pos_xref.extract.file_reader import FileReader

class Customer():
    def __init__(self, acct_num, norm, orig, bill_to_state, bill_to_postal_code, fuzzy_matches):
        self.acct_num = acct_num
        self.norm = norm
        self.orig = orig
        self.bill_to_state = bill_to_state
        self.bill_to_postal_code = bill_to_postal_code
        self.fuzzy_matches = fuzzy_matches

    def __str__(self):
        return f" Account Number: {self.acct_num} ; Customer Name: {self.orig}"

class ProcessedOutput():
    def __init__(self, test_env):
        self.test_env = test_env
        self.fuzzy_matches_df = pd.DataFrame()
        self._prev_matches = {}
        self._direct_custs = pd.DataFrame()
        self._pos_custs = pd.DataFrame()
        self.name_map = {}

    def __str__(self):
        return f"Output data for Processed.csv"

    def _requirements(self):
        pm = PreviousMatches(self.test_env)
        pm.run()
        self._prev_matches = pm.lookup

        direct = FileReader(self.test_env, 'direct')
        direct.run()
        self._direct_custs = direct.df

        pos_sales = FileReader(self.test_env, 'pos_sales')
        pos_sales.run()
        self._pos_custs = pos_sales.df    

    def _fuzzy_match(self, norm, choices):
        '''
        Return fuzzy matches for a given customer, excluding matches previously completed
        args:
            norm: the normalized name version of the customer to search
            choices: the customers to query against
        '''
        raw_matches = process.extract(query=norm, choices=choices, score_cutoff=88, limit=20)
        new_matches = []
        
        for match in raw_matches:
            orig = self.name_map[match[0]]
            if not orig in self._prev_matches[norm]: # exclude previous matches
                '''append original, non-normalized name to return matches'''
                new_matches.append(match)

        return new_matches

    def _build_name_maps(self) -> Dict:
        '''
        build a name map from normalized_name to customer_name (dict(str:str))
        TODO: does this potentially overwrite something unexpected?
        '''
        self.name_map = {norm : orig for norm, orig in zip(self._pos_custs['normalized_name'], self._pos_custs['customer_name'])}

    def _matching_engine(self):
        '''
        Generate fuzzy match column
        '''
         # fuzzy matching for direct to pos
        self._direct_custs['fuzzy_matches'] = self._direct_custs['normalized_name'].apply(
            lambda norm: 
            self._fuzzy_match(
                norm, 
                self._pos_custs['normalized_name']
                )
            )
        
        # fuzzy matching for pos to pos
        self._pos_custs['fuzzy_matches'] = self._pos_custs['normalized_name'].apply(
            lambda norm: 
            self._fuzzy_match(
                norm, 
                self._pos_custs['normalized_name']
                )
            )

    def _build_output_dfs(self):
        '''
            Convert fuzzy matches into output data frame; building cross reference (one to one)
        '''
        temp_df = pd.concat([self._pos_custs, self._direct_custs])

        # fill customer class
        customers = []
        for index, row in temp_df.iterrows():                
            customers.append(Customer(row['acct_num'], row['normalized_name'], row['customer_name'], 
                                      row['bill_to_state'], row['bill_to_postal_code'], row['fuzzy_matches']))
        
        # create output df
        for cust in customers:
            for fuzzy_match in cust.fuzzy_matches:
                match_score = fuzzy_match[1]
                row_index = len(self.fuzzy_matches_df)
                self.fuzzy_matches_df.loc[row_index, 'acct_num'] = cust.acct_num
                self.fuzzy_matches_df.loc[row_index, 'normalized_name'] = cust.norm
                self.fuzzy_matches_df.loc[row_index, 'customer_name'] = cust.orig
                self.fuzzy_matches_df.loc[row_index, 'bill_to_state'] = cust.bill_to_state
                self.fuzzy_matches_df.loc[row_index, 'bill_to_postal_code'] = cust.bill_to_postal_code
                self.fuzzy_matches_df.loc[row_index, 'fuzzy_match'] = self.name_map[fuzzy_match[0]]
                self.fuzzy_matches_df.loc[row_index, 'match_score'] = round(fuzzy_match[1],2)
                if match_score == 100:                
                    self.fuzzy_matches_df.loc[row_index, 'match_type'] = "self_match"
                else:
                    self.fuzzy_matches_df.loc[row_index, 'match_type'] = "fuzzy_match"    

    def format_output_dfs(self):
        self.fuzzy_matches_df.sort_values(by=['normalized_name'], inplace=True)

    def run(self):
        self._requirements()
        self._build_name_maps()
        self._matching_engine()
        self._build_output_dfs()
        self.format_output_dfs()
    