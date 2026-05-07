import pytest
from backend.generator import market_scout_research, growth_hacker_strategy

def test_market_scout_research():
    title = "AI in Healthcare"
    content = "New AI models are helping doctors diagnose diseases faster."
    niche, research = market_scout_research(title, content)

    assert niche in [
        "Healthcare AI Diagnostics",
        "E-commerce Inventory Optimization",
        "Niche Developer Copilots (GameDev/Blockchain)",
        "Sustainable Supply Chain tracking",
        "Remote Team Productivity Automation"
    ]
    assert "detected" in research.lower()

def test_growth_hacker_strategy():
    niche = "Healthcare AI Diagnostics"
    research = "Detected high-growth potential."
    strategy, monetization = growth_hacker_strategy(niche, research)

    assert "revenue" in monetization.lower()
    assert len(strategy) > 10
