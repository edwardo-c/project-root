import pandas as pd
from pos_xref.extract.previous_matches import PreviousMatches
from pos_xref.extract.file_reader import FileReader

# may need a customer class? would make it easier to fill the output df
# use self.acct_num instead of trying to to paste it from a previous row.
# just seems cleaner, but adds a layer of complexity without being re-usable.
# GET IT TO WORK FIRST, THEN REFACTOR


class ProcessedOutput():
    def __init__(self, test_env):
        self.output_df = pd.DataFrame()
        self.test_env = test_env
    
    def __str__(self):
        return f"Output data including fuzzy matches"

    def _prepare_processed_output(self):
        '''
        prepares the output data frame to  be manually inspected by user
        excludes self matches and previous matches
        '''
        # get the new customers data frame
        customers = 

        # get the previous matches look up structure
        pm = PreviousMatches(self.test_env)

    def fuzzy_match_direct_to_pos(self):
        direct = FileReader(self.test_env, 'direct')
        direct.run()

        pos_sales = FileReader(self.test_env, 'pos_sales')
        pos_sales.run()
        
        ...
    
    def fuzzy_match_pos():
        ...

    def new_sold_to_data(self):
        
        
        ...

    def run():
        ...
    ...