# Spark Autonomous Revenue System

Spark is a full-stack autonomous product that researches high-demand trends, generates business opportunities, and deploys an intelligence mesh to execute revenue-generating strategies 24/7.

## Features

- **Intelligence Mesh:** Multi-agent architecture (Market Scout, Growth Hacker, Auto-Executor).
- **LLM-Ready Brain:** Modular engine using semantic market analysis, ready for OpenAI/Anthropic.
- **Autonomous Yield:** Targeted hourly revenue of $100 - $500 across active pipelines.
- **Secure Monitoring:** Protected command center with live audit logs.

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite, BeautifulSoup4
- **Frontend:** React, TypeScript, Vite, Tailwind CSS

## Getting Started

### 1. Prerequisites
- Python 3.12+
- Node.js 22+

### 2. Setup Backend
```bash
cd backend
pip install -r requirements.txt
# Set your Admin Secret for security
export ADMIN_SECRET=your_custom_secret
PYTHONPATH=. python3 -m backend.init_db
uvicorn backend.main:app --reload
```

### 3. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🚀 How to Start Generating Revenue

### Step 1: Link Payment Gateway
Link your Google Pay QR code url using the secured settings endpoint:

```bash
curl -X PATCH http://localhost:8000/settings \
     -H "Content-Type: application/json" \
     -H "X-Admin-Secret: your_custom_secret" \
     -d '{"key": "google_pay_qr", "value": "https://path-to-your-qr.png"}'
```

### Step 2: Activate Intelligence Mesh
Trigger the first autonomous cycle to deploy the agents:

```bash
curl -X POST http://localhost:8000/trigger
```

### Step 3: Monitor Work & Yield
Open `http://localhost:5173` to view the live dashboard.
- **Live Revenue Stream:** Real-time counter of yield and optimization bonuses.
- **Intelligence Audit Log:** Verified trail of agent actions and market research.

### Step 4: Scale
As the system matures, the **Optimization Bonus** (visible on the dashboard) will increase, scaling your hourly yield automatically.

---

## Testing
Run all intelligence and revenue tests:
```bash
PYTHONPATH=. pytest
```
