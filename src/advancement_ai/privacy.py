"""Privacy boundary between record-level data and AI providers."""

from __future__ import annotations

import json
from typing import Any

DIRECT_IDENTIFIERS = {"constituent_id", "constituent_name", "email", "gift_id", "name"}
SAFE_KEYS = {
    "fiscal_year", "total_giving", "unique_donors", "total_gifts", "average_gift",
    "median_gift", "largest_gift", "new_donors", "retained_donors", "recovered_donors",
    "lybunt_donors", "sybunt_donors", "donor_retention_rate", "yoy_giving_change",
    "yoy_donor_change", "top_10_percent_donor_concentration", "data_quality_score",
    "annual", "by_campaign", "by_designation", "by_gift_officer", "by_state",
    "by_class_year", "monthly_trend", "gift_size_distribution",
}


def privacy_safe_context(analytics: dict[str, Any]) -> dict[str, Any]:
    """Allow only aggregate result keys and recursively remove identifier-shaped keys."""
    def scrub(value: Any) -> Any:
        if isinstance(value, dict):
            return {k: scrub(v) for k, v in value.items() if k.lower() not in DIRECT_IDENTIFIERS}
        if isinstance(value, list):
            return [scrub(item) for item in value]
        return value
    return scrub({k: v for k, v in analytics.items() if k in SAFE_KEYS})


def serialized_safe_context(analytics: dict[str, Any]) -> str:
    return json.dumps(privacy_safe_context(analytics), sort_keys=True, default=str)

