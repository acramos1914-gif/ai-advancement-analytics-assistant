"""Governed fundraising metrics calculated only from cleaned records."""

from __future__ import annotations

from typing import Any

import pandas as pd


def _records(series: pd.Series, value_name: str = "total_giving") -> list[dict[str, Any]]:
    return [{"name": str(k), value_name: round(float(v), 2)} for k, v in series.items()]


def _lifecycle(df: pd.DataFrame, current: int) -> dict[str, Any]:
    years = df.groupby("constituent_id")["fiscal_year"].apply(lambda x: set(map(int, x)))
    current_set = {d for d, ys in years.items() if current in ys}
    prior_set = {d for d, ys in years.items() if current - 1 in ys}
    historical = {d for d, ys in years.items() if any(y < current - 1 for y in ys)}
    new = {d for d in current_set if min(years[d]) == current}
    retained = current_set & prior_set
    recovered = {d for d in current_set if d not in prior_set and d in historical}
    lybunt = prior_set - current_set
    sybunt = {d for d, ys in years.items() if any(y < current for y in ys) and current not in ys}
    retention = len(retained) / len(prior_set) if prior_set else 0.0
    return {
        "new_donors": len(new), "retained_donors": len(retained),
        "recovered_donors": len(recovered), "lybunt_donors": len(lybunt),
        "sybunt_donors": len(sybunt), "donor_retention_rate": round(retention, 4),
    }


def calculate_analytics(df: pd.DataFrame, validation_counts: dict[str, int] | None = None) -> dict[str, Any]:
    if df.empty:
        raise ValueError("No valid gift records are available for analysis.")
    latest = int(df["fiscal_year"].max())
    annual = df.groupby("fiscal_year").agg(total_giving=("gift_amount", "sum"), donors=("constituent_id", "nunique"), gifts=("gift_id", "nunique")).sort_index()
    annual_records = [{"fiscal_year": int(i), **{k: round(float(v), 2) if k == "total_giving" else int(v) for k, v in row.items()}} for i, row in annual.iterrows()]
    latest_row = annual.loc[latest]
    prior = annual.loc[latest - 1] if latest - 1 in annual.index else None
    yoy_giving = ((latest_row.total_giving / prior.total_giving) - 1) if prior is not None and prior.total_giving else None
    yoy_donors = ((latest_row.donors / prior.donors) - 1) if prior is not None and prior.donors else None
    donor_totals = df.groupby("constituent_id")["gift_amount"].sum().sort_values(ascending=False)
    top_n = max(1, int(len(donor_totals) * 0.1 + 0.999))
    concentration = donor_totals.head(top_n).sum() / donor_totals.sum()
    bad = sum((validation_counts or {}).get(k, 0) for k in ["invalid_amounts", "invalid_dates", "missing_constituent_ids", "duplicate_gift_ids", "nonpositive_gifts"])
    received = max((validation_counts or {}).get("rows_received", len(df)), 1)
    metrics: dict[str, Any] = {
        "fiscal_year": latest,
        "total_giving": round(float(df.gift_amount.sum()), 2),
        "unique_donors": int(df.constituent_id.nunique()),
        "total_gifts": int(df.gift_id.nunique()),
        "average_gift": round(float(df.gift_amount.mean()), 2),
        "median_gift": round(float(df.gift_amount.median()), 2),
        "largest_gift": round(float(df.gift_amount.max()), 2),
        "yoy_giving_change": round(float(yoy_giving), 4) if yoy_giving is not None else None,
        "yoy_donor_change": round(float(yoy_donors), 4) if yoy_donors is not None else None,
        "top_10_percent_donor_concentration": round(float(concentration), 4),
        "data_quality_score": round(max(0.0, 1 - bad / received), 4),
        "annual": annual_records,
    }
    metrics.update(_lifecycle(df, latest))
    for col, key in [("campaign", "by_campaign"), ("designation", "by_designation"), ("gift_officer", "by_gift_officer"), ("state", "by_state"), ("preferred_class_year", "by_class_year")]:
        if col in df:
            metrics[key] = _records(df.groupby(col, dropna=False).gift_amount.sum().sort_values(ascending=False))
    monthly = df.assign(month=df.gift_date.dt.to_period("M").astype(str)).groupby("month").gift_amount.sum()
    metrics["monthly_trend"] = _records(monthly)
    bins = pd.cut(df.gift_amount, [0, 100, 500, 1000, 5000, 25000, float("inf")], labels=["$1–$99", "$100–$499", "$500–$999", "$1K–$4,999", "$5K–$24,999", "$25K+"])
    metrics["gift_size_distribution"] = [{"name": str(k), "gift_count": int(v)} for k, v in bins.value_counts(sort=False).items()]
    return metrics
