import pytest
from backend.generator import analyze_trend, generate_report

def test_analyze_trend():
    title = "AI in Healthcare"
    content = "New AI models are helping doctors diagnose diseases faster."
    analysis = analyze_trend(title, content)

    assert "AI" in analysis["title"]
    assert "High" == analysis["market_potential"]
    assert "AI" in analysis["description"]

def test_generate_report():
    class MockOpp:
        def __init__(self, title):
            self.title = title

    opp = MockOpp("Autonomous AI Solution")
    plan, assets = generate_report(opp)

    assert "# Business Plan: Autonomous AI Solution" in plan
    assert "logo_prompt" in assets
