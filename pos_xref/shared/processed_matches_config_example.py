TEST_PROCESSED_FILE_PATH = r"C:\My\test\Path\processed_matches.csv" # for repo, point to .\data\processed\proccessed_matches.csv
PROD_PROCESSED_FILE_PATH = r"H:\My\Prod\Path\processed_matches.csv" # not used in repo, for internal prod only

class ProcessedMatches():
    def __init__(self, test_env):
        self.test_env = test_env
        self.ws = "processed_matches"
        self.file_type = "processed_matches"

    def file_path(self):
        if self.test_env:
            return TEST_PROCESSED_FILE_PATH
        else:
            return PROD_PROCESSED_FILE_PATH
    
    def header_row(self):
        return 0
    
    def expected_columns(self):
        return ['acct_num',	'normalized_name',	'customer_name',
                'acct_group', 'bill_to_state', 	'bill_to_postal_code',
                'match_type']
