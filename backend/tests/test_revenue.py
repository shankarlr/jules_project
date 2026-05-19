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
    # Add a mock opportunity marked as Prime Path
    opp = Opportunity(title="Test Opp", description="Test Desc", market_potential="High", is_prime_path=1)
    db.add(opp)
    db.commit()

    await generate_revenue(db)

    revenue = db.query(Revenue).all()
    assert len(revenue) > 0
    # New logic: base_yield = 40 * complexity * multiplier
    # multiplier for High is 2.5. Complexity for "Test Desc" is 1.
    # Base = 100. Performance 0.85 - 1.15.
    assert revenue[0].amount >= 80
    assert revenue[0].amount <= 250 # approx 150 * 1.4 * 1.1

@pytest.mark.asyncio
async def test_update_agent_activities(db):
    await update_agent_activities(db)

    agents = db.query(AgentStatus).all()
    assert len(agents) == 3
    assert agents[0].name in ["Market Scout", "Growth Hacker", "Auto-Executor"]
    assert agents[0].current_task is not None
    assert agents[0].status in ["Acting", "Thinking", "Optimizing"]
