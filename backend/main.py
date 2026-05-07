from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import get_db
from . import models, worker
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
import uvicorn
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Spark Autonomous API")

# Security: ADMIN_SECRET must be set in the environment for production
ADMIN_SECRET = os.getenv("ADMIN_SECRET")
if not ADMIN_SECRET:
    logger.warning("ADMIN_SECRET not set in environment. Using default 'dev_secret' for development.")
    ADMIN_SECRET = "dev_secret"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SettingsUpdate(BaseModel):
    key: str
    value: str

async def verify_admin(x_admin_secret: str = Header(None)):
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Unauthorized: Invalid Admin Secret")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Spark Backend is running"}

@app.get("/trends")
def get_trends(db: Session = Depends(get_db)):
    return db.query(models.Trend).order_by(models.Trend.created_at.desc()).all()

@app.get("/opportunities")
def get_opportunities(db: Session = Depends(get_db)):
    return db.query(models.Opportunity).order_by(models.Opportunity.created_at.desc()).all()

@app.get("/reports/{opportunity_id}")
def get_report(opportunity_id: int, db: Session = Depends(get_db)):
    return db.query(models.Report).filter(models.Report.opportunity_id == opportunity_id).first()

@app.post("/trigger")
async def trigger_autonomy(background_tasks: BackgroundTasks):
    background_tasks.add_task(worker.run_autonomous_cycle)
    return {"message": "Autonomous Intelligence Cycle triggered in background"}

@app.get("/revenue/stats")
def get_revenue_stats(db: Session = Depends(get_db)):
    total_revenue = db.query(func.sum(models.Revenue.amount)).scalar() or 0

    # Last hour revenue
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    hourly_revenue = db.query(func.sum(models.Revenue.amount)).filter(models.Revenue.created_at >= one_hour_ago).scalar() or 0

    return {
        "total_revenue": round(total_revenue, 2),
        "hourly_revenue": round(hourly_revenue, 2)
    }

@app.get("/agents")
def get_agents(db: Session = Depends(get_db)):
    return db.query(models.AgentStatus).all()

@app.get("/audit")
def get_audit_logs(db: Session = Depends(get_db), limit: int = 20):
    return db.query(models.AuditLog).order_by(models.AuditLog.created_at.desc()).limit(limit).all()

@app.get("/settings")
def get_settings(db: Session = Depends(get_db)):
    settings = db.query(models.GlobalSettings).all()
    return {s.key: s.value for s in settings}

@app.patch("/settings", dependencies=[Depends(verify_admin)])
def update_settings(update: SettingsUpdate, db: Session = Depends(get_db)):
    setting = db.query(models.GlobalSettings).filter(models.GlobalSettings.key == update.key).first()
    if not setting:
        setting = models.GlobalSettings(key=update.key, value=update.value)
        db.add(setting)
    else:
        setting.value = update.value
    db.commit()
    return {"message": f"Global Setting '{update.key}' updated successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
