from fastapi import FastAPI, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import get_db
from . import models, worker
import uvicorn

app = FastAPI(title="Spark Autonomous API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return {"message": "Autonomous cycle triggered in background"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
