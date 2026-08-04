"""Deterministic standardization and record exclusion."""

from __future__ import annotations

import pandas as pd

VALID_STATES = set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC".split())


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    data = df.copy()
    for column in data.columns:
        if data[column].dtype == object:
            data[column] = data[column].fillna("").astype(str).str.strip()
    data["gift_amount"] = pd.to_numeric(data["gift_amount"].str.replace(r"[$,]", "", regex=True), errors="coerce")
    data["gift_date"] = pd.to_datetime(data["gift_date"], errors="coerce")
    data["constituent_id"] = data["constituent_id"].fillna("").astype(str).str.strip()
    data["gift_id"] = data["gift_id"].fillna("").astype(str).str.strip()
    invalid = (
        data["gift_amount"].isna() | data["gift_amount"].le(0) |
        data["gift_date"].isna() | data["constituent_id"].eq("") | data["gift_id"].eq("")
    )
    duplicate = data["gift_id"].duplicated(keep="first")
    excluded = {
        "invalid_or_incomplete": int(invalid.sum()),
        "duplicate_gift_ids": int((duplicate & ~invalid).sum()),
        "total_excluded": int((invalid | duplicate).sum()),
    }
    data = data.loc[~(invalid | duplicate)].copy()
    if "state" in data:
        data["state"] = data["state"].str.upper()
        data.loc[~data["state"].isin(VALID_STATES), "state"] = "Unknown"
    if "preferred_class_year" in data:
        years = pd.to_numeric(data["preferred_class_year"], errors="coerce")
        data["preferred_class_year"] = years.where(years.between(1900, 2100)).astype("Int64")
    for col in ["campaign", "designation", "gift_officer", "gift_type", "constituent_type", "city"]:
        if col in data:
            data[col] = data[col].replace("", "Unassigned" if col == "gift_officer" else "Unknown")
    data["fiscal_year"] = data["gift_date"].dt.year + (data["gift_date"].dt.month >= 7).astype(int)
    return data.sort_values("gift_date").reset_index(drop=True), excluded

