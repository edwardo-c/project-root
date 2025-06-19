import pytest
import pandas as pd

@pytest.fixture
def direct_test_data():
    return pd.DataFrame(
        {
            'Customer ID': [
                'AMZ135664',
            ],
            'Customer Name': [
                'AMAZON DIRECT INC',
            ],
            'State': [
                'BC'
            ],
            'Postal Code': [
                'V5Y 1L3'
            ]
        }
    )


@pytest.fixture
def foreign_test_data():
    return pd.DataFrame(
       {
           'SoldToName':[
               'AMAZON LLC',
               'AMAZON DC CORP'
           ],
           'BillToCustomerZip': [
               '44720-6902',
               'V5Y 1L3'
           ],
           'BillToCustomerState':[
               'OH',
               'BC'
           ]
       } 
    )

    