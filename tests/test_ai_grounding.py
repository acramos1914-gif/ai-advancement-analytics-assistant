from advancement_ai.analytics import calculate_analytics
from advancement_ai.demo_provider import DemoProvider


def test_demo_summary_is_deterministic(clean):
    a = calculate_analytics(clean)
    provider = DemoProvider()
    first = provider.generate("summary", a)
    assert first == provider.generate("summary", a)
    assert "$2,100" in first
    assert "Calculated facts" in first and "Recommendations" in first


def test_unsupported_question_is_rejected(clean):
    answer = DemoProvider().answer("What is Alex's email address?", calculate_analytics(clean))
    assert "only answer approved questions" in answer

