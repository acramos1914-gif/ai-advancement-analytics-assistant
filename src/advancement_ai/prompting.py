"""Grounded prompts and controlled-question policy."""

from __future__ import annotations

from .privacy import serialized_safe_context

ALLOWED_TOPICS = ("year", "giving", "campaign", "retention", "donor", "designation", "gift", "quality", "leadership", "officer", "state", "class")


def question_is_supported(question: str) -> bool:
    text = question.strip().lower()
    return bool(text) and any(term in text for term in ALLOWED_TOPICS)


def build_prompt(task: str, analytics: dict) -> str:
    context = serialized_safe_context(analytics)
    return f"""You are an advancement analytics advisor. Use ONLY the TRUSTED_RESULTS below.
All numerical facts must be copied from TRUSTED_RESULTS. Do not calculate, estimate, infer,
or invent numbers. Never claim access to donor-level records. Clearly label calculated facts,
interpretation, and recommendations. If evidence is insufficient, say so.

TASK: {task}
TRUSTED_RESULTS: {context}
"""

