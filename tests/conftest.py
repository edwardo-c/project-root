import pytest
import pandas as pd

@pytest.fixture
def primary_test_data():
    return pd.DataFrame(
        {
            "acct_num": [
                "AMZ135664",
            ],
            "customer_name": [
                "AMAZON DIRECT",
            ],
        }
    )


@pytest.fixture
def foreign_test_data():
    return pd.DataFrame(
       {
           "acct_num":[
               None,
               None,
           ],
           'customer_name':[
               'AMAZON LLC',
               'AMAZON DC'
           ]
       } 
    )

    