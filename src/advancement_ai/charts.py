"""Reusable Plotly executive charts."""

from __future__ import annotations

import pandas as pd
import plotly.express as px

NAVY = "#17324D"
GOLD = "#C49A47"


def annual_chart(analytics: dict):
    frame = pd.DataFrame(analytics["annual"])
    return px.line(frame, x="fiscal_year", y="total_giving", markers=True, color_discrete_sequence=[NAVY], labels={"total_giving": "Giving", "fiscal_year": "Fiscal year"})


def category_chart(records: list[dict], title: str, limit: int = 10):
    frame = pd.DataFrame(records[:limit]).sort_values("total_giving")
    return px.bar(frame, x="total_giving", y="name", orientation="h", title=title, color_discrete_sequence=[GOLD], labels={"total_giving": "Giving", "name": ""})
