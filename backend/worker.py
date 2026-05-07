import asyncio
import logging
from .scraper import scrape_trends
from .generator import process_new_trends

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_autonomous_cycle():
    """
    Runs the full autonomous loop:
    1. Scrape latest trends.
    2. Analyze trends and generate opportunities.
    3. Generate detailed reports.
    """
    logger.info("Starting Autonomous Cycle...")
    try:
        await scrape_trends()
        logger.info("Scraping completed.")
        await process_new_trends()
        logger.info("Analysis and Generation completed.")
    except Exception as e:
        logger.error(f"Error in Autonomous Cycle: {e}")

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
