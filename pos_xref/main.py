from pos_xref.shared.pos_config import get_raw_pos_customers

def main():
    year = 2024
    test_env = True  # Set to False if you're pointing at prod files
    
    try:
        df = get_raw_pos_customers(year=year, test_env=test_env)
        print(df.head())
        print(f"Successfully loaded data for {year}")
    except Exception as e:
        print(f"Failed to load data for {year}")

if __name__ == "__main__":
    main()
