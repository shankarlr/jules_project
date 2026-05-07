import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models import Opportunity, Revenue, AgentStatus
from backend.revenue_engine import generate_revenue, update_agent_activities

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_revenue.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.mark.asyncio
async def test_generate_revenue(db):
    # Add a mock opportunity
    opp = Opportunity(title="Test Opp", description="Test Desc", market_potential="High")
    db.add(opp)
    db.commit()

    await generate_revenue(db)

    revenue = db.query(Revenue).all()
    assert len(revenue) > 0
    # Base yield for High is 80, performance 0.9-1.3, bonus starts at 1.0
    assert revenue[0].amount >= 70 # approx 80 * 0.9
    assert revenue[0].amount <= 110 # approx 80 * 1.3

@pytest.mark.asyncio
async def test_update_agent_activities(db):
    await update_agent_activities(db)

    agents = db.query(AgentStatus).all()
    assert len(agents) == 3
    assert agents[0].name in ["Market Scout", "Growth Hacker", "Auto-Executor"]
    assert agents[0].current_task is not None
    assert agents[0].status in ["Thinking", "Acting", "Optimizing"]
