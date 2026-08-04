from advancement_ai.analytics import calculate_analytics
from advancement_ai.demo_provider import DemoProvider
from advancement_ai.reporting import build_markdown_report, build_pdf_report, kpi_csv


def test_reports_generate(clean):
    a = calculate_analytics(clean)
    narrative = DemoProvider().generate("summary", a)
    markdown = build_markdown_report(a, narrative)
    pdf = build_pdf_report(a, narrative)
    csv = kpi_csv(a)
    assert "Executive Advancement" in markdown
    assert pdf.startswith(b"%PDF")
    assert b"total_giving" in csv

