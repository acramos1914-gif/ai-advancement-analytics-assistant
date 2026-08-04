"""Render lightweight recruiter-facing previews from trusted sample metrics."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from advancement_ai.analytics import calculate_analytics
from advancement_ai.cleaning import clean_data
from advancement_ai.validation import validate_data

NAVY, GOLD, BG, WHITE, TEXT, MUTED = "#17324D", "#C49A47", "#F4F7FA", "#FFFFFF", "#1E2D3D", "#5F6F7F"


def font(size: int, bold: bool = False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    try:
        return ImageFont.truetype(name, size)
    except OSError:
        return ImageFont.load_default()


def base(title: str, subtitle: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (1400, 820), BG)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1400, 92), fill=NAVY)
    draw.text((54, 24), title, fill=WHITE, font=font(30, True))
    draw.text((54, 105), subtitle, fill=MUTED, font=font(18))
    return image, draw


def card(draw, x, y, w, h, label, value, note=""):
    draw.rounded_rectangle((x, y, x + w, y + h), 14, fill=WHITE, outline="#D9E1E8", width=2)
    draw.text((x + 22, y + 20), label.upper(), fill=MUTED, font=font(14, True))
    draw.text((x + 22, y + 52), value, fill=NAVY, font=font(29, True))
    if note: draw.text((x + 22, y + 96), note, fill="#39735B", font=font(14))


def save_dashboard(a):
    im, d = base("Advancement Analytics Assistant", "Executive dashboard · fictional portfolio dataset")
    values = [("Total giving", f"${a['total_giving']:,.0f}"), ("Donors", f"{a['unique_donors']:,}"), ("Gifts", f"{a['total_gifts']:,}"), ("Retention", f"{a['donor_retention_rate']:.1%}"), ("Data quality", f"{a['data_quality_score']:.1%}")]
    for i, (label, value) in enumerate(values): card(d, 54 + i * 260, 150, 236, 125, label, value)
    d.text((54, 325), "Fiscal-year giving", fill=TEXT, font=font(22, True))
    annual = a["annual"]
    maximum = max(r["total_giving"] for r in annual)
    points = []
    for i, row in enumerate(annual):
        x = 95 + i * 185; y = 650 - int(row["total_giving"] / maximum * 245)
        points.append((x, y)); d.text((x - 18, 675), str(row["fiscal_year"]), fill=MUTED, font=font(14))
    d.line(points, fill=GOLD, width=6)
    for x, y in points: d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=NAVY)
    d.text((980, 325), "Top campaigns", fill=TEXT, font=font(22, True))
    top = a["by_campaign"][:5]; maxv = top[0]["total_giving"]
    for i, row in enumerate(top):
        y = 380 + i * 62; d.text((980, y), row["name"], fill=TEXT, font=font(15)); d.rectangle((980, y + 25, 980 + int(330 * row["total_giving"] / maxv), y + 42), fill=GOLD)
    im.save(ROOT / "screenshots" / "dashboard.png")


def save_panel(filename, title, subtitle, cards, bullets):
    im, d = base(title, subtitle)
    for i, (label, value, note) in enumerate(cards): card(d, 54 + i * 320, 155, 290, 130, label, value, note)
    d.rounded_rectangle((54, 330, 1346, 750), 14, fill=WHITE, outline="#D9E1E8", width=2)
    d.text((85, 365), "Key findings", fill=TEXT, font=font(24, True))
    y = 420
    for bullet in bullets:
        d.ellipse((88, y + 7, 98, y + 17), fill=GOLD); d.text((115, y), bullet, fill=TEXT, font=font(18)); y += 62
    im.save(ROOT / "screenshots" / filename)


def main():
    raw = pd.read_csv(ROOT / "data" / "sample" / "fictional_advancement_gifts.csv", dtype=str)
    validation = validate_data(raw); clean, excluded = clean_data(raw); a = calculate_analytics(clean, validation.counts)
    save_dashboard(a)
    save_panel("validation.png", "Upload & validation", "Transparent exceptions before analysis", [("Rows received", f"{len(raw):,}", "Source rows"), ("Clean rows", f"{len(clean):,}", "Ready for analytics"), ("Excluded", f"{excluded['total_excluded']:,}", "Never silently retained")], validation.warnings[:4])
    save_panel("executive_insights.png", "Grounded executive insights", "Demo mode · no API key required", [("Total giving", f"${a['total_giving']:,.0f}", "Calculated fact"), ("YOY giving", f"{a['yoy_giving_change']:+.1%}", "Calculated fact"), ("Quality", f"{a['data_quality_score']:.1%}", "Calculated fact")], ["AI explains the trusted Python result object.", "Interpretations are separated from calculated facts.", "Recommendations are clearly labeled for analyst review."])
    save_panel("donor_retention.png", "Donor retention analytics", f"Latest fiscal year {a['fiscal_year']}", [("Retained", f"{a['retained_donors']:,}", "Gave this year and last"), ("LYBUNT", f"{a['lybunt_donors']:,}", "Gave last year, not this year"), ("Recovered", f"{a['recovered_donors']:,}", "Returned after a gap"), ("Retention", f"{a['donor_retention_rate']:.1%}", "Retained ÷ prior-year donors")], ["Lifecycle status is calculated from fiscal-year gift history.", "No model assigns donor lifecycle categories.", "Use LYBUNT counts to prioritize renewal outreach."])
    save_panel("responsible_ai.png", "Responsible AI notice", "Privacy-safe by design", [("Direct IDs sent", "0", "Allow-list boundary"), ("Demo network calls", "0", "Deterministic templates"), ("Numeric source", "Python", "Governed result object")], ["Names, emails, constituent IDs, and gift IDs stay outside prompts.", "The live prompt forbids invented or newly calculated figures.", "All AI interpretation and recommendations require analyst review."])
    print("Generated five portfolio preview images from trusted sample metrics.")


if __name__ == "__main__":
    main()

