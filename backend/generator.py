from .database import SessionLocal
from .models import Trend, Opportunity, Report
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulating an AI/NLP engine for zero-cost autonomous logic
def analyze_trend(trend_title, trend_content):
    """
    Analyzes a trend and generates an opportunity.
    In a production app, this could call an LLM API.
    For zero-cost/autonomous, we use a heuristic-based generator.
    """
    keywords = ["AI", "Crypto", "Remote", "Sustainable", "Health", "E-commerce", "Automation"]

    found_keywords = [k for k in keywords if k.lower() in trend_title.lower() or k.lower() in trend_content.lower()]

    if not found_keywords:
        found_keywords = ["Generic Innovation"]

    opportunity_title = f"Autonomous {found_keywords[0]} Solution for '{trend_title[:30]}...'"
    description = f"Based on the trend '{trend_title}', there is a high demand for {found_keywords[0]} driven services. This solution addresses the core problem by automating the workflow identified in the source."
    market_potential = "High" if len(found_keywords) > 1 else "Medium"

    return {
        "title": opportunity_title,
        "description": description,
        "market_potential": market_potential
    }

def generate_report(opportunity):
    """
    Generates a full business plan/report for an opportunity.
    """
    plan = f"""
    # Business Plan: {opportunity.title}

    ## Executive Summary
    This product leverages autonomous intelligence to solve problems in the {opportunity.title} space.

    ## Implementation Strategy
    1. Scrape data related to {opportunity.title}.
    2. Identify pain points.
    3. Deploy autonomous agents to handle customer inquiries.

    ## Monetization
    - Subscription model for enterprise users.
    - Pay-per-insight for individual consultants.
    """

    assets = json.dumps({
        "logo_prompt": f"Modern minimalist logo for {opportunity.title}",
        "landing_page_headline": f"Revolutionize your workflow with {opportunity.title}",
        "target_audience": "Tech-savvy professionals"
    })

    return plan, assets

async def process_new_trends():
    db = SessionLocal()
    try:
        # Get trends that don't have an opportunity yet
        trends = db.query(Trend).all()
        for trend in trends:
            existing_opp = db.query(Opportunity).filter(Opportunity.trend_id == trend.id).first()
            if not existing_opp:
                logger.info(f"Analyzing trend: {trend.title}")
                analysis = analyze_trend(trend.title, trend.content)
                new_opp = Opportunity(
                    trend_id=trend.id,
                    title=analysis["title"],
                    description=analysis["description"],
                    market_potential=analysis["market_potential"]
                )
                db.add(new_opp)
                db.flush() # Get the new ID

                # Generate report for the new opportunity
                plan, assets = generate_report(new_opp)
                new_report = Report(
                    opportunity_id=new_opp.id,
                    plan=plan,
                    assets=assets
                )
                db.add(new_report)
        db.commit()
    except Exception as e:
        logger.error(f"Error in InsightGenerator: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(process_new_trends())
