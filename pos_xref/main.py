from pos_xref.shared.combine_input_data import return_input_data

# for public repo, test_env should be True from project_root/run_pos_xref.py

def main(test_env:bool, year):
    
    try:
        df = return_input_data(test_env)
        print(df.head())
        print(f"Successfully loaded direct and pos customer data")

    except Exception as e:
        print(f"Failed to load input data")

if __name__ == "__main__":
    main()
