TEST_MATCHES_FILE_PATH = r"C:\My\test\Path\matches.csv" # for repo, point this to .\data\output\matches.csv
PROD_MATCHES_FILE_PATH = r"H:\My\Prod\Path\processed_matches.csv" # not needed for repo, used in internal prod

class Matches():
    def __init__(self, test_env):
        self.test_env = test_env
        self.ws = "matches"
        self.file_type = "matches"

    def file_path(self):
        if self.test_env:
            return TEST_MATCHES_FILE_PATH
        else:
            return PROD_MATCHES_FILE_PATH
    
    def header_row(self):
        return 0
    
    def expected_columns(self):
        return ['acct_num',	'normalized_name',	'customer_name',
                'acct_group', 'bill_to_state', 	'bill_to_postal_code',
                'match_type']
