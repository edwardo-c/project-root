# from typing import List
# import pandas as pd

# def get_customer_classes(df:pd.DataFrame):
#     '''
#     build a dictionary to avoid duplications of customer names
#     '''
#     customer_dict = {}
#     for _, row in df.iterrows():
#         acct_num = row['acct_num']
#         cust_name = row['customer_name']
#         acct_group = row['acct_group']
#         bill_to_zip = row['bill_to_postal_code']
#         bill_to_state = row['bill_to_state']
        
#         if not cust_name in customer_dict:
#             customer_dict[cust_name] = {
#                 'acct_num': acct_num,
#                 'acct_group': acct_group,
#                 'bill_to_postal_code': bill_to_zip,
#                 'bill_to_state': bill_to_state
#                 }
            
#     return customer_dict

# class Customer:
#     def __init__(self, original_name: str, bill_to_postal_code, 
#                  id: str, 
#                  ):
#         self.original_name = original_name
#         self.normalized_name = original_name
#         self.id = id
#         self.fuzzy_matches = "" #TODO: function to return fuzzy matches
#         self.postal_code = bill_to_postal_code

#     def __repr__(self):
#         return f"Customer(name={self.original_name}, id={self.id})"