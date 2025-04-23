from pos_xref.shared.combine_input_data import return_input_data
import pos_xref.extract.matching_pipeline as mp
# for public repo, test_env should be True from project_root/run_pos_xref.py

def main(test_env:bool, year):
    
    # try:

    # get current customer data (all POS and direct)
    df = return_input_data(test_env) # get input data

    # get previous matches
    previous_matches = mp.get_previous_matches(test_env=test_env)

    # fill export data frame with new matches (exclude previous matches and self matches)
    

    print(previous_matches)
        
    # except Exception as e:
    #     print(f"Failed to load input data")

if __name__ == "__main__":
    main()
