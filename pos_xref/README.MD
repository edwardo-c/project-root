# POS Xref Pipeline

This project is designed to safely extract key customer data from Master POS (point of sale) Excel files and direct customers file
stored on a shared network.  

It's part of a larger internal tooling effort to standardize and automate cross-referencing of POS customer name variations and linking back to direct customers.

> **Problem this solves**:  
> *How much has customer X purchased through direct AND POS (distributors' supplied data)?*

---

## Features

- Safe reading of shared Excel files without locking them
- Extracts and standardizes fields for years 2020–2025:
  - `acct_num`  (only for direct accounts)
  - `sold_to_name` (the name in the POS data)
  - `acct_group` (only for direct accounts)
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

    cp pos_xref/pos_config_example.py pos_xref/pos_config.py
    cp pos_xref/pos_config_example.py pos_xref/direct_config.py

5. Open pos_config.py and direct_config:

    Ensure TEST_DIR in pos_config.py points to .\pos_xref\data\raw\ where test files are included
    Ensure TEST_FILE_PATH in direct_config.py points to .\pos_xref\data\raw\direct_customers_export.xlsx

6. Run the script

    python -m run_pos_xref.py
