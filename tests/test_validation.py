from io import BytesIO

import pandas as pd
import pytest

from advancement_ai.cleaning import clean_data
from advancement_ai.validation import read_upload, validate_data


def test_missing_columns():
    result = validate_data(pd.DataFrame({"gift_id": ["G1"]}))
    assert not result.valid
    assert "Missing required columns" in result.errors[0]


def test_invalid_values_and_duplicate_handling(raw_data):
    bad = raw_data.copy()
    bad.loc[len(bad)] = bad.iloc[0]
    bad.loc[len(bad)] = {"constituent_id":"", "constituent_name":"X", "gift_id":"GX", "gift_date":"bad", "gift_amount":"nope"}
    result = validate_data(bad)
    cleaned, excluded = clean_data(bad)
    assert result.counts["invalid_amounts"] == 1
    assert result.counts["invalid_dates"] == 1
    assert result.counts["duplicate_gift_ids"] == 1
    assert excluded["total_excluded"] == 2
    assert cleaned.gift_id.is_unique


def test_upload_rejections():
    with pytest.raises(ValueError, match="Unsupported"):
        read_upload(BytesIO(b"x"), "bad.txt")
    with pytest.raises(ValueError, match="empty"):
        read_upload(BytesIO(b""), "empty.csv")

