"""Portable Markdown, CSV, and PDF report generation."""

from __future__ import annotations

from io import BytesIO

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def build_markdown_report(a: dict, narrative: str) -> str:
    return f"""# Executive Advancement Analytics Report

**Latest fiscal year:** {a['fiscal_year']}  
**Synthetic data only:** Every person and transaction represented is fictional.

## Calculated KPI summary

| KPI | Result |
|---|---:|
| Total giving | ${a['total_giving']:,.2f} |
| Unique donors | {a['unique_donors']:,} |
| Total gifts | {a['total_gifts']:,} |
| Average gift | ${a['average_gift']:,.2f} |
| Median gift | ${a['median_gift']:,.2f} |
| Donor retention | {a['donor_retention_rate']:.1%} |
| LYBUNT donors | {a['lybunt_donors']:,} |
| Data quality score | {a['data_quality_score']:.1%} |

## Executive narrative

{narrative}

---
AI-generated interpretation and recommendations require analyst review. All numerical results above were calculated in Python.
"""


def build_pdf_report(a: dict, narrative: str) -> bytes:
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter, rightMargin=.7 * inch, leftMargin=.7 * inch, topMargin=.7 * inch, bottomMargin=.7 * inch)
    styles = getSampleStyleSheet()
    story = [Paragraph("Executive Advancement Analytics Report", styles["Title"]), Spacer(1, 12)]
    for label, value in [
        ("Latest fiscal year", str(a["fiscal_year"])), ("Total giving", f"${a['total_giving']:,.2f}"),
        ("Unique donors", f"{a['unique_donors']:,}"), ("Total gifts", f"{a['total_gifts']:,}"),
        ("Donor retention", f"{a['donor_retention_rate']:.1%}"), ("Data quality score", f"{a['data_quality_score']:.1%}"),
    ]:
        story.append(Paragraph(f"<b>{label}:</b> {value}", styles["BodyText"]))
    story.extend([Spacer(1, 16), Paragraph("Executive narrative", styles["Heading2"])])
    for paragraph in narrative.replace("**", "").split("\n\n"):
        story.append(Paragraph(paragraph.replace("\n", "<br/>"), styles["BodyText"]))
        story.append(Spacer(1, 8))
    story.append(Paragraph("Synthetic data only. AI interpretation requires analyst review.", styles["Italic"]))
    doc.build(story)
    return output.getvalue()


def kpi_csv(a: dict) -> bytes:
    scalar = {k: v for k, v in a.items() if not isinstance(v, (list, dict))}
    return pd.DataFrame([{"metric": k, "value": v} for k, v in scalar.items()]).to_csv(index=False).encode()

