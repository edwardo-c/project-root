from pos_xref.transformations.normalize_data import normalize_df

def run_matching_engine(primary_df, foreign_df):

    # 1. normalize data
    primary_df = normalize_df(primary_df)
    foreign_df = normalize_df(foreign_df)

    # 2. fuzzy match
    


    # 3. output results

    ...
