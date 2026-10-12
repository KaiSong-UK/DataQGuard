from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Datasource(Base):
    __tablename__ = "datasources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # postgresql, mysql, mongodb, etc.
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    database = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)  # Should be encrypted
    ssl_mode = Column(String(50), default="prefer")
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    rules = relationship("Rule", back_populates="datasource")


class Rule(Base):
    __tablename__ = "rules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    datasource_id = Column(Integer, ForeignKey("datasources.id"))
    table_name = Column(String(255), nullable=False)
    rule_type = Column(String(50), nullable=False)  # completeness, accuracy, consistency, timeliness, uniqueness
    rule_config = Column(JSON, nullable=False)  # Store rule-specific config
    schedule = Column(String(100), default="0 */4 * * *")  # Cron expression
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    datasource = relationship("Datasource", back_populates="rules")
    executions = relationship("RuleExecution", back_populates="rule")


class RuleExecution(Base):
    __tablename__ = "rule_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(Integer, ForeignKey("rules.id"))
    status = Column(String(50), default="pending")  # pending, running, success, failed
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    total_rows = Column(Integer)
    failed_rows = Column(Integer)
    pass_rate = Column(Float)
    error_message = Column(Text)
    details = Column(JSON)  # Detailed results
    
    rule = relationship("Rule", back_populates="executions")


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    rule_id = Column(Integer, ForeignKey("rules.id"))
    execution_id = Column(Integer, ForeignKey("rule_executions.id"))
    severity = Column(String(20), default="warning")  # info, warning, error, critical
    message = Column(Text, nullable=False)
    channel = Column(String(50), default="email")  # email, slack, webhook, dingtalk
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
