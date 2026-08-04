import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import pandas as pd
import pytest

from advancement_ai.cleaning import clean_data


@pytest.fixture
def raw_data():
    return pd.DataFrame([
        {"constituent_id":"A", "constituent_name":"Alex", "gift_id":"G1", "gift_date":"2023-08-01", "gift_amount":"100", "campaign":"Annual", "designation":"General", "gift_officer":"One", "state":"NY", "preferred_class_year":"2000"},
        {"constituent_id":"A", "constituent_name":"Alex", "gift_id":"G2", "gift_date":"2024-08-01", "gift_amount":"200", "campaign":"Annual", "designation":"General", "gift_officer":"One", "state":"NY", "preferred_class_year":"2000"},
        {"constituent_id":"B", "constituent_name":"Blair", "gift_id":"G3", "gift_date":"2022-08-01", "gift_amount":"300", "campaign":"Capital", "designation":"Library", "gift_officer":"Two", "state":"MA", "preferred_class_year":"1999"},
        {"constituent_id":"B", "constituent_name":"Blair", "gift_id":"G4", "gift_date":"2024-09-01", "gift_amount":"400", "campaign":"Capital", "designation":"Library", "gift_officer":"Two", "state":"MA", "preferred_class_year":"1999"},
        {"constituent_id":"C", "constituent_name":"Casey", "gift_id":"G5", "gift_date":"2023-09-01", "gift_amount":"500", "campaign":"Annual", "designation":"General", "gift_officer":"", "state":"ZZ", "preferred_class_year":""},
        {"constituent_id":"D", "constituent_name":"Devon", "gift_id":"G6", "gift_date":"2024-10-01", "gift_amount":"600", "campaign":"Annual", "designation":"General", "gift_officer":"One", "state":"CA", "preferred_class_year":"2005"},
    ])


@pytest.fixture
def clean(raw_data):
    return clean_data(raw_data)[0]

