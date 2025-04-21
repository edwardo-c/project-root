import re

def normalize_name(name:str) -> str:
    '''
    normalizes seller name by returning lower case, removes non letter characters
    strips white space, and removes common suffixes. 
    '''

    # remove special characters
    pattern = re.compile(r'[^a-zA-Z0-9\s]')
    name_minus_spec_chars = re.sub(pattern, '', name)

    # remove suffixes
    suffixes = ['inc','grp','co','ltd', 'llc', 'corp', 'corporation']
    suffixes_pattern = r'\b(?:' + '|'.join(suffixes) + r')\b'

    pattern = re.compile(suffixes_pattern, flags=re.IGNORECASE)
    name_minus_suffixes = re.sub(pattern, '', name_minus_spec_chars)

    return name_minus_suffixes.strip().lower()

def clean_zip_code():
    '''TODO: turns a zip code into a 5 digit zip or standardizes canada zips (upper case, with a space)'''
    pass