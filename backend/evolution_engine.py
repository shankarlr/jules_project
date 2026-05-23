import os
import importlib
import logging
import inspect
from .database import SessionLocal
from .models import Opportunity, AuditLog
from .generator import brain

logger = logging.getLogger(__name__)

class EvolutionEngine:
    """
    The Recursive Self-Evolution Engine.
    Enables agents to write, test, and deploy their own code modules
    to optimize revenue generation.
    """
    EVOLUTION_DIR = "backend/evolution"

    @classmethod
    async def evolve(cls):
        """
        Main evolution loop:
        1. Analyze current performance.
        2. Identify code bottlenecks.
        3. Generate optimized Python logic.
        4. Deploy to the evolution directory.
        """
        db = SessionLocal()
        try:
            # Find the most efficient Prime Path
            prime = db.query(Opportunity).filter(Opportunity.is_prime_path == 1).order_by(Opportunity.version.desc()).first()
            if not prime:
                return

            version = prime.version
            niche = prime.title.replace("Prime Path: ", "")

            # 1. Self-Analysis Prompting
            # In a real scenario, we'd pass the actual content of current evolution modules
            code_prompt = f"""
            Target: Optimize revenue for {niche} (Goal: $500/hr).
            Current Efficiency: {prime.efficiency_score:.2f}.
            Task: Write a Python class 'RevenueStrategy' with a method 'calculate_yield(base_amount)'
            that implements a compounding growth algorithm based on version {version}.
            The code must be valid Python and return a float.
            """

            logger.info(f"Agent is evolving code for version {version+1}...")

            # 2. Code Generation (Simulated for safety, but structure is real)
            # In production, brain.generate_code() would return the string below
            evolved_code = f"""
class RevenueStrategy:
    \"\"\"
    Evolved Revenue Strategy v{version+1}
    Niche: {niche}
    \"\"\"
    def calculate_yield(self, base_amount: float) -> float:
        # Recursive Compounding Logic evolved by the agent
        efficiency_multiplier = {prime.efficiency_score + 0.05}
        version_bonus = {version * 0.1}
        return base_amount * (1.0 + efficiency_multiplier + version_bonus)
"""

            # 3. Deployment (Persistence)
            module_name = f"strategy_v{version+1}"
            file_path = os.path.join(cls.EVOLUTION_DIR, f"{module_name}.py")

            with open(file_path, "w") as f:
                f.write(evolved_code)

            # 4. Audit Trail
            log = AuditLog(
                agent_name="CodeOptimizer",
                action=f"Self-evolved core logic to v{version+1}. Deployed to {file_path}"
            )
            db.add(log)
            db.commit()

            logger.info(f"Evolution complete. New module deployed: {module_name}")
            return module_name

        except Exception as e:
            logger.error(f"Evolution Engine Error: {e}")
            db.rollback()
        finally:
            db.close()

    @classmethod
    def get_latest_strategy(cls):
        """
        Dynamically loads the latest evolved strategy module.
        """
        files = [f for f in os.listdir(cls.EVOLUTION_DIR) if f.startswith("strategy_v") and f.endswith(".py")]
        if not files:
            return None

        # Sort by version number
        latest_file = sorted(files, key=lambda x: int(x.split("_v")[1].split(".py")[0]), reverse=True)[0]
        module_name = latest_file.replace(".py", "")

        try:
            # Use importlib for dynamic loading
            module = importlib.import_module(f"backend.evolution.{module_name}")
            # Reload to ensure we get the latest version if it was updated
            importlib.reload(module)

            if hasattr(module, "RevenueStrategy"):
                return module.RevenueStrategy()
        except Exception as e:
            logger.error(f"Failed to load evolved strategy {module_name}: {e}")

        return None
