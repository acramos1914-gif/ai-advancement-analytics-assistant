from advancement_ai.privacy import privacy_safe_context, serialized_safe_context
from advancement_ai.prompting import build_prompt


def test_identifiers_removed():
    unsafe = {"total_giving": 10, "constituent_id": "C1", "email": "a@example.org", "annual": [{"fiscal_year": 2025, "constituent_name": "Alex"}]}
    safe = privacy_safe_context(unsafe)
    payload = serialized_safe_context(unsafe)
    assert safe == {"total_giving": 10, "annual": [{"fiscal_year": 2025}]}
    assert "C1" not in payload and "example.org" not in payload and "Alex" not in payload


def test_prompt_is_grounded():
    prompt = build_prompt("Summarize", {"total_giving": 123, "email": "secret@example.org"})
    assert "TRUSTED_RESULTS" in prompt
    assert "Do not calculate" in prompt
    assert "123" in prompt
    assert "secret" not in prompt

