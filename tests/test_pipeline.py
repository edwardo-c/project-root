import pandas as pd

''' 
test matching logic
'''

def test_one_to_many():
    '''
    should output 9 rows after matching sequence
    3 self matches because of the 3 unique names
    6 fuzzy matches because each entry matches the other two
    '''
    
    direct_data = {'acct_num':['AMZ135664'], 
              'customer_name': ['AMAZON DIRECT']}
    direct_df = pd.DataFrame(direct_data)

    foreign_data = {'acct_num':[None, None], 
                    'customer_name':['AMAZON LLC', 'AMAZON DC']}
    foreign_df = pd.DataFrame(foreign_data)

    output_df = pd.concat([direct_df, foreign_df])
    
    assert len(output_df) == 9 # should fail since len(output_df) == 3