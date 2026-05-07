from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, timezone

class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    source = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    trend_id = Column(Integer, ForeignKey("trends.id"))
    title = Column(String)
    description = Column(Text)
    market_potential = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"))
    plan = Column(Text)
    assets = Column(Text) # JSON string of suggested assets
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Revenue(Base):
    __tablename__ = "revenue"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class AgentStatus(Base):
    __tablename__ = "agent_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    current_task = Column(Text)
    status = Column(String)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class GlobalSettings(Base):
    __tablename__ = "global_settings"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(Text)

class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String)
    action = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
