from typing import Dict
from collections import defaultdict
from rapidfuzz import process
import pandas as pd
from pos_xref.extract.previous_matches import PreviousMatches
from pos_xref.extract.file_reader import FileReader

# may need a customer class? would make it easier to fill the output df
# use self.acct_num instead of trying to to paste it from a previous row.



'''
In order to update processed.csv - 

fuzzy match direct to pos
    Exclude previous matches
    convert to output df

fuzzy match pos to pos - concat with output df
    Exclude self_matches
    convert to output df

'''

class Customer():
    ...

class ProcessedOutput():
    def __init__(self, test_env):
        self.test_env = test_env
        self.output_df = pd.DataFrame()
        self._prev_matches = {}
        self._direct_custs = pd.DataFrame()
        self._pos_custs = pd.DataFrame()

    def __str__(self):
        return f"Output data for Processed.csv"

    def _requirements(self):
        '''
        save the previous matches look up structure, used to eliminated duplicate matches in fuzzy matching
        defaultdict(set)
        '''
        pm = PreviousMatches(self.test_env)
        pm.run()
        self._prev_matches = pm.lookup

        direct = FileReader(self.test_env, 'direct')
        direct.run()
        self._direct_custs = direct.df

        pos_sales = FileReader(self.test_env, 'pos_sales')
        pos_sales.run()
        self._pos_custs = pos_sales.df    

    def _fuzzy_match(self, norm, choices, name_map:Dict):
        '''
        Return fuzzy matches for a given customer, excluding matches previously completed
        args:
            all_customers: the customers to query against

        Query against normalized names; return customer_name
        exclude previously matched
        TODO: exclude self matches for pos to pos 
        '''

        raw_matches = process.extract(query=norm, choices=choices, score_cutoff=88, limit=20)
        new_matches = []
        
        # remove previous matches
        for match in raw_matches:
            orig = name_map[match[0]]
            if not orig in self._prev_matches[norm]: 
                '''append original, non-normalized name to return matches'''
                new_matches.append(orig)

        return new_matches

    def _build_name_map(self) -> Dict:
        '''
        builds a name map from normalized_name to customer_name
        '''
        return {norm : orig for norm, orig in zip(self._pos_custs['normalized_name'], self._pos_custs['customer_name'])}

    def _matching_engine(self):
        '''
        Generate fuzzy match column
        '''
         # fuzzy matching for direct to pos
        name_map = self._build_name_map() # used for mapping back to original name
        self._direct_custs['fuzzy_matches'] = self._direct_custs['normalized_name'].apply(
                                                                                        lambda norm: 
                                                                                        self._fuzzy_match(
                                                                                            norm, 
                                                                                            self._pos_custs['normalized_name'],
                                                                                            name_map)
                                                                                        )
        # fuzzy matching for pos to pos
        self._pos_custs['fuzzy_matches'] = self._pos_custs['normalized_name'].apply(
                                                                                    lambda norm: 
                                                                                    self._fuzzy_match(
                                                                                        norm, 
                                                                                        self._pos_custs['normalized_name'],
                                                                                        name_map)
                                                                                        )
        
        # TODO: do you need fuzzy matching for pos back to direct? this could close the matching loop
        # and would help the user match pos back to direct since all connections would be completed


    def _build_output(self):
        '''match direct to pos'''
        
        '''match pos to pos'''

        '''store output df as self.output_df'''
        ...

    def run(self):
        self._requirements()
        self._matching_engine()
    