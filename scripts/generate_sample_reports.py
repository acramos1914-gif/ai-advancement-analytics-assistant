"""Create committed recruiter-facing sample outputs from the fictional dataset."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from advancement_ai.analytics import calculate_analytics
from advancement_ai.cleaning import clean_data
from advancement_ai.demo_provider import DemoProvider
from advancement_ai.reporting import build_markdown_report, build_pdf_report
from advancement_ai.validation import validate_data


def main() -> None:
    raw = pd.read_csv(ROOT / "data" / "sample" / "fictional_advancement_gifts.csv", dtype=str)
    validation = validate_data(raw)
    clean, _ = clean_data(raw)
    analytics = calculate_analytics(clean, validation.counts)
    narrative = DemoProvider().generate("Generate executive summary", analytics)
    out = ROOT / "reports" / "samples"
    out.mkdir(parents=True, exist_ok=True)
    (out / "demo_ai_summary.md").write_text("# Demo AI summary\n\n" + narrative + "\n", encoding="utf-8")
    (out / "executive_report.md").write_text(build_markdown_report(analytics, narrative), encoding="utf-8")
    (out / "executive_report.pdf").write_bytes(build_pdf_report(analytics, narrative))
    print("Generated demo summary and executive Markdown/PDF reports.")


if __name__ == "__main__":
    main()

