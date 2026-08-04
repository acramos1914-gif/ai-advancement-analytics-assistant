"""Input validation with business-friendly issue reporting."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import BinaryIO

import pandas as pd

REQUIRED_COLUMNS = {
    "constituent_id", "constituent_name", "gift_id", "gift_date", "gift_amount"
}
OPTIONAL_COLUMNS = {
    "constituent_type", "preferred_class_year", "city", "state", "email",
    "gift_type", "campaign", "designation", "gift_officer",
}
MAX_FILE_BYTES = 25 * 1024 * 1024


@dataclass
class ValidationResult:
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    counts: dict[str, int] = field(default_factory=dict)


def read_upload(file: BinaryIO, filename: str, size: int | None = None) -> pd.DataFrame:
    suffix = Path(filename).suffix.lower()
    if suffix not in {".csv", ".xlsx"}:
        raise ValueError("Unsupported file type. Upload a CSV or XLSX file.")
    if size is not None and size > MAX_FILE_BYTES:
        raise ValueError("File exceeds the 25 MB upload limit.")
    try:
        frame = pd.read_csv(file, dtype=str) if suffix == ".csv" else pd.read_excel(file, dtype=str)
    except pd.errors.EmptyDataError as exc:
        raise ValueError("The uploaded file is empty.") from exc
    if frame.empty:
        raise ValueError("The uploaded file contains no records.")
    frame.columns = [str(c).strip().lower() for c in frame.columns]
    return frame


def validate_data(df: pd.DataFrame) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    missing = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing:
        errors.append("Missing required columns: " + ", ".join(missing))
        return ValidationResult(False, errors, warnings, {"rows_received": len(df)})

    amount = pd.to_numeric(df["gift_amount"].astype(str).str.replace(r"[$,]", "", regex=True), errors="coerce")
    dates = pd.to_datetime(df["gift_date"], errors="coerce")
    ids = df["constituent_id"].fillna("").astype(str).str.strip()
    gifts = df["gift_id"].fillna("").astype(str).str.strip()
    counts = {
        "rows_received": int(len(df)),
        "invalid_amounts": int(amount.isna().sum()),
        "invalid_dates": int(dates.isna().sum()),
        "missing_constituent_ids": int(ids.eq("").sum()),
        "duplicate_gift_ids": int((gifts.duplicated(keep="first") & gifts.ne("")).sum()),
        "nonpositive_gifts": int(amount.le(0).fillna(False).sum()),
    }
    for key, label in [
        ("invalid_amounts", "malformed gift amount(s)"),
        ("invalid_dates", "invalid gift date(s)"),
        ("missing_constituent_ids", "missing constituent ID(s)"),
        ("duplicate_gift_ids", "duplicate gift ID(s)"),
        ("nonpositive_gifts", "zero or negative gift(s)"),
    ]:
        if counts[key]:
            warnings.append(f"{counts[key]:,} {label} will be excluded.")
    return ValidationResult(True, errors, warnings, counts)
