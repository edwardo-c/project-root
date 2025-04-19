from pos_xref.shared.pos_config import get_raw_pos_customers
from pos_xref.shared.direct_config import capture_direct_customers_df

def main(test_env:bool, year):
    
    try:
        df = get_raw_pos_customers(year=year, test_env=test_env)
        print(df.head())
        print(f"Successfully loaded data for {year}")

        direct_df = capture_direct_customers_df(test_env)
        print(direct_df.head())
        print(f"Successfully loaded direct customer data")

    except Exception as e:
        print(f"Failed to load data for {year}")

if __name__ == "__main__":
    main()
