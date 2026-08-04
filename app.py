"""Streamlit application for trustworthy advancement analytics."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from advancement_ai.analytics import calculate_analytics
from advancement_ai.charts import annual_chart, category_chart
from advancement_ai.cleaning import clean_data
from advancement_ai.demo_provider import DemoProvider
from advancement_ai.live_provider import LiveProvider
from advancement_ai.reporting import build_markdown_report, build_pdf_report, kpi_csv
from advancement_ai.validation import read_upload, validate_data

load_dotenv()
st.set_page_config(page_title="Advancement Analytics Assistant", page_icon="📊", layout="wide")
st.markdown("""<style>
.stApp {background:#F6F8FA}.block-container{padding-top:1.5rem;max-width:1280px}
[data-testid="stMetric"]{background:white;border:1px solid #DDE3E9;border-radius:10px;padding:14px}
h1,h2,h3{color:#17324D}.notice{background:#FFF8E8;border-left:5px solid #C49A47;padding:1rem;border-radius:6px}
</style>""", unsafe_allow_html=True)

st.title("Advancement Analytics Assistant")
st.caption("Trusted fundraising metrics. Privacy-safe AI interpretation. Executive-ready reporting.")
st.markdown('<div class="notice"><b>Responsible AI notice:</b> Numerical results are calculated in Python. AI interpretation and recommendations require analyst review. Direct identifiers are never sent to the AI provider.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Workspace")
    mode = st.radio("AI mode", ["Demo (no API key)", "Live AI"], help="Demo mode is deterministic and free.")
    uploaded = st.file_uploader("Upload gifts", type=["csv", "xlsx"])
    use_sample = st.button("Load fictional sample", use_container_width=True)
    st.caption("Maximum 25 MB. CSV and XLSX only.")

sample_path = ROOT / "data" / "sample" / "fictional_advancement_gifts.csv"
if use_sample:
    st.session_state["use_sample"] = True

df = None
source = None
try:
    if uploaded:
        df = read_upload(uploaded, uploaded.name, uploaded.size)
        source = uploaded.name
    elif st.session_state.get("use_sample") and sample_path.exists():
        df = pd.read_csv(sample_path, dtype=str)
        source = "fictional_advancement_gifts.csv"
except ValueError as exc:
    st.error(str(exc))

home, validation_tab, dashboard, insights, ask, export = st.tabs(["Home", "Upload & validation", "Dashboard", "AI insights", "Ask the analyst", "Export"])
with home:
    st.subheader("From CRM export to governed executive insight")
    st.write("Upload a Salesforce-style gift export, validate and standardize it, calculate governed KPIs, then use a privacy-safe AI layer to explain—not invent—the results.")
    c1, c2, c3 = st.columns(3)
    c1.info("**1 · Validate**\n\nClear exclusions and a transparent quality score.")
    c2.info("**2 · Calculate**\n\nDeterministic fundraising and lifecycle metrics.")
    c3.info("**3 · Explain**\n\nOnly aggregate results cross the AI boundary.")
    st.markdown("**Privacy statement:** Uploaded records remain in the local Streamlit process. Names, emails, constituent IDs, and gift IDs are excluded from AI prompts.")

if df is None:
    for tab in [validation_tab, dashboard, insights, ask, export]:
        with tab:
            st.info("Upload a CSV/XLSX file or load the included fictional sample from the sidebar.")
    st.stop()

validation = validate_data(df)
if not validation.valid:
    with validation_tab:
        for error in validation.errors: st.error(error)
    st.stop()
cleaned, excluded = clean_data(df)
analytics = calculate_analytics(cleaned, validation.counts)
provider = DemoProvider()
if mode == "Live AI":
    try:
        provider = LiveProvider()
    except ValueError as exc:
        st.sidebar.warning(str(exc) + " Falling back to demo mode.")

with validation_tab:
    st.subheader(f"Validation · {source}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows received", f"{len(df):,}")
    c2.metric("Clean rows", f"{len(cleaned):,}")
    c3.metric("Excluded", f"{excluded['total_excluded']:,}")
    st.success("Required columns are present and the dataset is ready for analysis.")
    for warning in validation.warnings: st.warning(warning)
    st.dataframe(cleaned.head(100), use_container_width=True, hide_index=True)

with dashboard:
    st.subheader("Executive dashboard")
    cols = st.columns(6)
    for col, label, value in zip(cols, ["Total giving", "Donors", "Gifts", "Average gift", "Retention", "Quality"], [f"${analytics['total_giving']:,.0f}", f"{analytics['unique_donors']:,}", f"{analytics['total_gifts']:,}", f"${analytics['average_gift']:,.0f}", f"{analytics['donor_retention_rate']:.1%}", f"{analytics['data_quality_score']:.1%}"]): col.metric(label, value)
    left, right = st.columns(2)
    left.plotly_chart(annual_chart(analytics), use_container_width=True)
    right.plotly_chart(category_chart(analytics["by_campaign"], "Campaign performance"), use_container_width=True)
    st.subheader("Donor lifecycle")
    life = st.columns(5)
    for col, label, key in zip(life, ["New", "Retained", "Recovered", "LYBUNT", "SYBUNT"], ["new_donors", "retained_donors", "recovered_donors", "lybunt_donors", "sybunt_donors"]): col.metric(label, f"{analytics[key]:,}")
    category = st.selectbox("Explore performance", ["Designation", "Gift officer", "State", "Class year"])
    key = {"Designation": "by_designation", "Gift officer": "by_gift_officer", "State": "by_state", "Class year": "by_class_year"}[category]
    st.plotly_chart(category_chart(analytics[key], f"Giving by {category.lower()}"), use_container_width=True)

tasks = ["Generate executive summary", "Explain year-over-year performance", "Identify donor-retention risks", "Recommend campaign actions", "Summarize data-quality risks", "Create leadership talking points"]
with insights:
    st.subheader("Grounded executive insights")
    task = st.selectbox("Insight brief", tasks)
    if st.button("Generate insight", type="primary"):
        st.session_state["narrative"] = provider.generate(task, analytics)
    narrative = st.session_state.get("narrative", DemoProvider().generate(tasks[0], analytics))
    st.markdown(narrative)

with ask:
    st.subheader("Ask the analyst")
    st.caption("Supported topics: performance, campaigns, designations, retention, gift officers, geography, class year, and data quality.")
    question = st.text_input("Question", placeholder="What drove the year-over-year change?")
    if st.button("Answer question"):
        st.markdown(provider.answer(question, analytics))
    st.markdown("**Try:** Which campaigns need attention? · What are the largest retention risks? · What should leadership prioritize next?")

with export:
    st.subheader("Export results")
    narrative = st.session_state.get("narrative", DemoProvider().generate(tasks[0], analytics))
    markdown = build_markdown_report(analytics, narrative)
    st.download_button("Download executive Markdown", markdown, "executive_report.md", "text/markdown")
    st.download_button("Download executive PDF", build_pdf_report(analytics, narrative), "executive_report.pdf", "application/pdf")
    st.download_button("Download cleaned CSV", cleaned.to_csv(index=False).encode(), "cleaned_gifts.csv", "text/csv")
    st.download_button("Download KPI CSV", kpi_csv(analytics), "kpi_summary.csv", "text/csv")

