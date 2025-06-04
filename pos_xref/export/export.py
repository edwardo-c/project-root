import pandas as pd
from pos_xref.extract.process_output import ProcessedOutput
from pos_xref.extract.file_reader import FileReader

'''
Goal: export results for user to manually review and align
results: 
    fuzzy matches: primary name against foreign names
    self matches:  primary name against normalized primary name 
        contained within class: processed_output (po.self_matches)
'''

class FileExporter():
    def __init__(self, test_env):
        self.test_env = test_env
        self.processed_output_info = FileReader
        self.fuzzy_output = pd.DataFrame
        self.output = pd.DataFrame
    def __str__():
        return f"Export pipeline, last step before user manual review"
    
    def _requirements(self):
        '''
            get output file info to overwrite existing
            TODO: set up version control to archive prior to overwrite
        '''
        pi = FileReader(self.test_env, 'processed')
        pi.run()
        self.processed_info = pi

        po = ProcessedOutput(self.test_env)
        po.run()
        self.fuzzy_output = po.fuzzy_matches_df

    def _build_output_df(self):
        # consolidating new (fuzzy) output, with existing processed df
        # pi.processed_info.df contains the original, non matched data set
        # this retains the work in progress - intentionally does not overwrite what is in processed.csv
        self.output = pd.concat([self.fuzzy_output, 
                                 self.processed_info.df]).drop_duplicates().reset_index(drop=True)
    
    def _export(self):
        self.output.to_csv(self.processed_info.file_path, index=False)

    def run(self):
        self._requirements()
        self._build_output_df()
        # self._export() # intentionally left _export() out to review output