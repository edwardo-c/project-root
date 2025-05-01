# POS Xref Pipeline

This project is designed to safely extract customer names from Master POS (point of sale) and direct customers Excel files
stored on a shared network.

It's part of a larger internal tooling effort to standardize and automate cross-referencing of POS customer name variations and linking back to direct customers.

> **Problem this solves**:  
> *How much has customer X purchased through direct AND indirect (POS [distributor's supplied data])?*

---

## Features

- Safe reading of shared Excel files without locking them
- Extracts and standardizes fields for years 2020–2025:
  - `acct_num`  (only for direct accounts)
  - `customer_name` (the name in the POS data)
  - `acct_group` 
  - `bill_to_zip` 
  - `bill_to_state`
- Clean, modular project structure with virtual environment

---

## How to Run

1. **Clone the repo and navigate to the project root:**

   ```bash
   cd project_root

2. Create and activate the virtual environment:
    
    python -m venv pos_xref/venv
    source pos_xref/venv/Scripts/activate  # For Windows

3. Install required packages:

    pip install -r pos_xref/requirements.txt

4. Copy the config templates:

    cp pos_xref/shared/pos_config_example.py pos_xref/pos_config.py
    cp pos_xref/shared/direct_config_example.py pos_xref/direct_config.py
    cp pos_xref/shared/matches_config_example.py pos_xref/matches_config.py
    cp pos_xref/shared/processed_matches_config_example.py processed_matches_config.py 

5. Open pos_config.py, direct_config.py, matches_config.py, & processed_matches_config.py:

    Ensure TEST_DIR in pos_config.py points to .\pos_xref\data\raw\
    Ensure TEST_FILE_PATH in direct_config.py points to .\pos_xref\data\raw\direct_customers_export.xlsx
    ENSURE TEST_MATCHES_FILE_PATH points to .\pos_xref\data\output\matches.csv
    ENSURE TEST_PROCESSED_FILE_PATH points to .\pos_xref\data\processed\proccessed_matches.csv

6. Run the script

    python -m run_pos_xref.py
