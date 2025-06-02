import pandas as pd
from pos_xref.extract.process_output import ProcessedOutput
from pos_xref.extract.file_reader import FileReader

class FileExporter():
    def __init__(self, test_env):
        self.test_env = test_env
        self.processed_output = ProcessedOutput
        self.processed_output_info = FileReader
    
    def __str__():
        return f"Export pipeline, last step before user manual review"
    
    def _requirements(self):
        ''' get outputs and output file info'''
        po = ProcessedOutput(self.test_env)
        po.run()
        self.processed_output = po

        pi = FileReader(self.test_env, 'processed')
        pi.run()
        self.processed_info = pi
    
    def _append_and_dedup(df1: pd.DataFrame, df2: pd.DataFrame):
        return pd.concat([df1, df2]).drop_duplicates(subset=['normalized_name', 'customer_name'])
    
    def _export(df: pd.DataFrame, file_path: str):
        df.to_csv(file_path, index=False)

    def pipeline(self):
        # capture existing files
        '''
        Updated processed file:
        - concatenate new processed with previous processed - drop duplicates
        '''
        # Export matches to be processed
        # col_subset = ['normalized_name', 'customer_name']
        new_processed = self._append_and_dedup(self.processed_output, 
                                               self.processed_info.df)
        

        self._export(new_processed)
        '''
        where do the self matches go? These are confirmed matches, 
        so they should go into the final output. This may take some
        more thought; self matches may need to be added to manually
        reviewed also in case they fall into a one-to-many relationships
        '''