import re
import pandas as pd

def normalize_df(df: pd.DataFrame):
    '''
    run data frame through the normalization process
    args:
        df: data frame to be normalized
    return:
        the data processed through the normalization functions
    '''
    df['normalized_name'] = df['customer_name'].apply(normalize_name)
    # TODO: make more module to accept different 'name' columns
    # TODO: normalize other colummns, left undone since these are 
    # 'nice to haves' in the system, not requirements
    return df

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

def normalize_postal_code(postal_code):
    '''converts a postal code into 5 digits or standardizes canada zips ("A1A 1A1")'''
    # TODO: convert the postal codes column to strings prior to clean_postal_code call
    postal_code = str(postal_code)

    # capture only letters, 3 letters = CA postal code, or first five digits
    ca_pattern = re.compile(r'[a-z]', flags=re.IGNORECASE)
    us_pattern = re.compile(r'[0-9]', flags=re.IGNORECASE)

    postal_code = postal_code.strip()
    letters = re.findall(ca_pattern, postal_code)
    numbers = re.findall(us_pattern, postal_code)

    if len(letters) == 3:
        # ensure 3 characters, a space, two characters structure
        return postal_code[:3] + ' ' + postal_code[-3:]
    elif len(numbers) >= 5:
        # ensure 5 digit only structure, remove dash and last 4 digits
        return ''.join(numbers[:5])
    else:
        return postal_code