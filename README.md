# Spark Autonomous

Spark is a full-stack autonomous product that researches high-demand trends and generates business opportunities and actionable reports without human intervention.

## Features

- **Autonomous Scraping:** Fetches real-time trends from major tech and news RSS feeds.
- **Intelligence Engine:** Analyzes trends to identify high-potential business opportunities.
- **Report Generation:** Creates detailed business plans and marketing asset prompts.
- **Modern Dashboard:** A React-based interface to visualize autonomous insights.

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite, BeautifulSoup4
- **Frontend:** React, TypeScript, Vite, Tailwind CSS

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 22+

### Setup Backend

1. Navigate to the `backend` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   PYTHONPATH=.. python3 -m backend.init_db
   ```
4. Run the server:
   ```bash
   uvicorn backend.main:app --reload
   ```

### Setup Frontend

1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## Autonomous Operation

The system can be triggered via the "Run Autonomous Cycle" button on the dashboard or by sending a POST request to `/trigger`. In production, this can be scheduled as a cron job to ensure 24/7 autonomous intelligence.
