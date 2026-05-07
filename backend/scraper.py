import httpx
from bs4 import BeautifulSoup
from .database import SessionLocal
from .models import Trend
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# A list of RSS feeds or news sites to scrape for trends
FEEDS = [
    "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "https://www.theverge.com/rss/index.xml",
    "https://techcrunch.com/feed/",
]

async def scrape_trends():
    db = SessionLocal()
    async with httpx.AsyncClient() as client:
        for url in FEEDS:
            try:
                logger.info(f"Scraping {url}")
                response = await client.get(url, timeout=10.0)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'xml')
                    items = soup.find_all('item')
                    for item in items[:5]: # Take top 5 from each feed
                        title = item.title.text if item.title else "No Title"
                        link = item.link.text if item.link else ""
                        description = item.description.text if item.description else ""

                        # Check if trend already exists
                        existing = db.query(Trend).filter(Trend.title == title).first()
                        if not existing:
                            new_trend = Trend(
                                title=title,
                                source=url,
                                content=description
                            )
                            db.add(new_trend)
                    db.commit()
            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
    db.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(scrape_trends())
