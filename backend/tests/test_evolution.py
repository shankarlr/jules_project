import pytest
import os
import shutil
from backend.evolution_engine import EvolutionEngine
from backend.database import Base, engine, SessionLocal
from backend.models import Opportunity

@pytest.fixture(scope="module", autouse=True)
def setup_evolution_dir():
    # Setup test evolution dir
    test_dir = "backend/evolution"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    yield
    # Cleanup after tests
    # We keep it for now as it's part of the app structure

@pytest.mark.asyncio
async def test_evolution_flow():
    db = SessionLocal()
    # 1. Create a Prime Path opportunity
    opp = Opportunity(
        title="Prime Path: Test Niche",
        description="Initial",
        version=1,
        efficiency_score=0.5,
        is_prime_path=1
    )
    db.add(opp)
    db.commit()

    # 2. Trigger evolution
    module_name = await EvolutionEngine.evolve()
    assert module_name is not None
    assert os.path.exists(f"backend/evolution/{module_name}.py")

    # 3. Test dynamic loading
    strategy = EvolutionEngine.get_latest_strategy()
    assert strategy is not None
    assert hasattr(strategy, "calculate_yield")

    yield_val = strategy.calculate_yield(100.0)
    assert yield_val > 100.0

    db.close()
