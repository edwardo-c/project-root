from pos_xref.shared.combine_input_data import return_input_data
from pos_xref.extract.matching_pipeline import get_previous_matches
# for public repo, test_env should be True from project_root/run_pos_xref.py

def main(test_env:bool, year):
    
    try:
        # get current customer data (all POS and direct)
        df = return_input_data(test_env) # get input data

        # TODO: generate fuzzy matches data frame
        previous_matches = get_previous_matches(test_env)

        # TODO: export matches to processed file 

        # User than manually confirms matches and mis matches

        # TODO: move processed to output data - seperating matches and those to be reviewed

        print(previous_matches)
        
    except Exception as e:
        print(f"Failed to load input data")

if __name__ == "__main__":
    main()
