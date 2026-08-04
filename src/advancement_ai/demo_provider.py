"""No-cost, deterministic narrative provider for portfolio demonstrations."""

from __future__ import annotations

from .ai_provider import AIProvider
from .prompting import question_is_supported


def _money(value: float) -> str:
    return f"${value:,.0f}"


def _pct(value: float | None) -> str:
    return "not available" if value is None else f"{value:+.1%}"


class DemoProvider(AIProvider):
    def generate(self, task: str, a: dict) -> str:
        campaigns = a.get("by_campaign", [])
        leader = campaigns[0] if campaigns else {"name": "No campaign", "total_giving": 0}
        facts = (
            f"**Calculated facts**\n\nFiscal year {a['fiscal_year']} is the latest period. "
            f"The validated dataset contains {_money(a['total_giving'])} across {a['total_gifts']:,} gifts "
            f"from {a['unique_donors']:,} donors. Year-over-year giving changed {_pct(a['yoy_giving_change'])}; "
            f"donor retention is {a['donor_retention_rate']:.1%}. {leader['name']} leads campaign giving "
            f"at {_money(leader['total_giving'])}. Data quality scored {a['data_quality_score']:.1%}."
        )
        interpretation = (
            "\n\n**AI interpretation**\n\n"
            f"The strongest signal for “{task}” is the combination of year-over-year performance, "
            "retention, and gift concentration. These measures should be reviewed together rather than in isolation."
        )
        recommendation = (
            "\n\n**Recommendations (analyst review required)**\n\n"
            f"Prioritize outreach to {a['lybunt_donors']:,} LYBUNT donors, review performance outside the leading "
            "campaign, and resolve remaining data-quality exceptions before leadership distribution."
        )
        return facts + interpretation + recommendation

    def answer(self, question: str, analytics: dict) -> str:
        if not question_is_supported(question):
            return "I can only answer approved questions supported by calculated fundraising, retention, campaign, designation, geographic, class-year, gift-officer, and data-quality results."
        return self.generate(question, analytics)

