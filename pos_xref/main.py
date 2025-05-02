from pos_xref.shared.combine_input_data import return_input_data
from pos_xref.extract.self_matches import update_self_matches
import pos_xref.extract.matching_pipeline as mp
# for public repo, test_env should be True from project_root/run_pos_xref.py

def main(test_env:bool, year):
    
    # try:

    # get current customer data (all POS and direct)
    all_custs_df = return_input_data(test_env) # get input data

    # fill self matches into data/output/matches.csv
    new_self_matches = update_self_matches(test_env, all_custs_df)

    # get previous matches lookup structure to reduce redundant matches check
    processed_matches = mp.get_processed_matches(test_env=test_env)

    # TODO: fill output data frame with fuzzy matching info

        # (exclude previous matches and self matches)
        # 


    

    print(processed_matches)
        
    # except Exception as e:
    #     print(f"Failed to load input data")

if __name__ == "__main__":
    main()
