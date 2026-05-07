import random
import logging
from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import Revenue, AgentStatus, Opportunity
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

AGENTS = [
    {"name": "Market Scout", "role": "Researcher", "tasks": [
        "Scanning tech news for high-growth trends...",
        "Analyzing market sentiment for AI tools...",
        "Identifying gaps in the current SaaS landscape...",
        "Evaluating competitor strategies in automation..."
    ]},
    {"name": "Growth Hacker", "role": "Strategist", "tasks": [
        "Designing viral loops for new opportunities...",
        "Optimizing conversion funnels for autonomous products...",
        "A/B testing monetization models...",
        "Refining target audience personas..."
    ]},
    {"name": "Auto-Executor", "role": "Executor", "tasks": [
        "Deploying autonomous micro-services...",
        "Integrating payment gateways...",
        "Automating customer support workflows...",
        "Scaling infrastructure for peak demand..."
    ]}
]

async def generate_revenue(db: Session):
    """
    Simulates hourly revenue generation based on Performance and Market Fit.
    """
    try:
        opportunities = db.query(Opportunity).all()
        if not opportunities:
            logger.info("No active pipelines. Revenue generation paused.")
            return

        # Calculate a "Scaling Factor" based on total previous revenue (simulating optimization over time)
        total_prev = db.query(func.sum(Revenue.amount)).scalar() or 0
        optimization_bonus = min(2.0, 1.0 + (total_prev / 5000)) # Up to 2x multiplier as system matures

        total_hourly_yield = 0
        for opp in opportunities:
            # Base yield depends on market potential
            base_yield = 80 if opp.market_potential == "High" else 30

            # Agent performance variation
            performance = random.uniform(0.9, 1.3)

            # Final contribution for this opportunity
            contribution = base_yield * performance * optimization_bonus

            new_revenue = Revenue(
                amount=round(contribution, 2),
                opportunity_id=opp.id
            )
            db.add(new_revenue)
            total_hourly_yield += contribution

        db.commit()
        logger.info(f"System Optimized: Current Hourly Yield ${total_hourly_yield:.2f} (Bonus: x{optimization_bonus:.2f})")
    except Exception as e:
        logger.error(f"Execution Error in Revenue Engine: {e}")
        db.rollback()

async def update_agent_activities(db: Session):
    """
    Updates AgentStatus with simulated "thinking" and "acting" logs.
    """
    try:
        for agent_info in AGENTS:
            agent = db.query(AgentStatus).filter(AgentStatus.name == agent_info["name"]).first()
            if not agent:
                agent = AgentStatus(
                    name=agent_info["name"],
                    role=agent_info["role"]
                )
                db.add(agent)

            agent.current_task = random.choice(agent_info["tasks"])
            agent.status = random.choice(["Thinking", "Acting", "Optimizing"])
            agent.updated_at = datetime.now(timezone.utc)

        db.commit()
        logger.info("Agent Intelligence Mesh updated.")
    except Exception as e:
        logger.error(f"Agent Coordination Error: {e}")
        db.rollback()
