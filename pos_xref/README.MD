# POS Xref Pipeline

Part of a larger internal tooling effort to standardize and automate cross-referencing of POS customer name variations back to direct customers;
as well as cross referencing name variations amongst pos customers. 

> **Problem this solves**:  
> *How much has customer X purchased through direct AND indirect (POS [distributor's supplied data])?*

**Example**:
Distributor_1 sells to 'AMAZON.COM'
Distributor_2 sells to 'amazon corporate'
Internally, sales go to 'AMAZON CORP'

**Solution**:
1. Safely extract customer names from Master POS (point of sale) and direct customers Excel files stored on a shared network.
2. Outputs fuzzy matches for user to manually scan and confirm crossreference
3. re-uploads the users confirmed matches to master cross reference file

---

## Features
- Safe reading of shared Excel files without locking them
- Extracts, standardizes fields, and fuzzy matches data for user to confirm cross referencing 
  - `acct_num`  
  - `customer_name`
  - `normalizzed_name`
  - `acct_group` 
  - `bill_to_postal_code` 
  - `bill_to_state`
- exclude previous matches/mismatches; reducing redundant user checks
- # TODO: automatic uploading of user matches to finalized csv
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

4. Copy the FileReader templates:

    cp pos_xref/shared/file_reader_example.py pos_xref/file_reader.py

5. Open file_reader.py:

    Ensure func(test_file_details) points to: .\pos_xref\data\... (see comments in func for specifics)

6. Run the main pipeline
    # TODO: instructions for how to run
    python -m run_pos_xref.py
