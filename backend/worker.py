import asyncio
import logging
from .scraper import scrape_trends
from .generator import process_new_trends
from .revenue_engine import generate_revenue, update_agent_activities
from .evolution_engine import EvolutionEngine
from .agents.optimizer import CodeOptimizer
from .database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_autonomous_cycle():
    """
    Runs the full autonomous loop:
    1. Scrape latest trends.
    2. Analyze trends and generate opportunities.
    3. Generate detailed reports.
    4. Generate revenue and update agent activities.
    """
    logger.info("Starting Autonomous Cycle...")
    db = SessionLocal()
    try:
        await scrape_trends()
        logger.info("Scraping completed.")
        await process_new_trends()
        logger.info("Analysis and Generation completed.")

        # 1. Code Evolution Phase
        optimizer = CodeOptimizer()
        await optimizer.analyze_and_propose()
        await EvolutionEngine.evolve()
        logger.info("Code Evolution cycle completed.")

        # 2. Performance-based Revenue and Agent logic
        await generate_revenue(db)
        await update_agent_activities(db)
        logger.info("Revenue optimization and Agent mesh updates completed.")
    except Exception as e:
        logger.error(f"Error in Autonomous Cycle: {e}")
    finally:
        db.close()

async def autonomous_worker_loop(interval_seconds=3600):
    """
    Infinite loop to run the autonomous cycle at set intervals.
    """
    while True:
        await run_autonomous_cycle()
        logger.info(f"Cycle finished. Sleeping for {interval_seconds} seconds.")
        await asyncio.sleep(interval_seconds)

if __name__ == "__main__":
    # For standalone testing, run one cycle
    asyncio.run(run_autonomous_cycle())
