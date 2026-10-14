from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.models import Alert, Rule, RuleExecution

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    # Total rules
    result = await db.execute(select(func.count()).select_from(Rule))
    total_rules = result.scalar()
    
    # Active rules
    result = await db.execute(select(func.count()).select_from(Rule).where(Rule.is_active == True))
    active_rules = result.scalar()
    
    # Total executions
    result = await db.execute(select(func.count()).select_from(RuleExecution))
    total_executions = result.scalar()
    
    # Recent executions
    result = await db.execute(
        select(RuleExecution).order_by(RuleExecution.started_at.desc()).limit(10)
    )
    recent_executions = result.scalars().all()
    
    # Unacknowledged alerts
    result = await db.execute(
        select(func.count()).select_from(Alert).where(Alert.is_sent == False)
    )
    pending_alerts = result.scalar()
    
    return {
        "total_rules": total_rules,
        "active_rules": active_rules,
        "total_executions": total_executions,
        "pending_alerts": pending_alerts,
        "recent_executions": [
            {
                "id": e.id,
                "rule_id": e.rule_id,
                "status": e.status,
                "started_at": e.started_at.isoformat() if e.started_at else None,
                "pass_rate": e.pass_rate
            }
            for e in recent_executions
        ]
    }


@router.get("/health-trend")
async def get_health_trend(days: int = 7, db: AsyncSession = Depends(get_db)):
    # TODO: Implement actual trend calculation from ClickHouse metrics
    # Return mock data for now
    return {
        "labels": [f"Day {i}" for i in range(days)],
        "datasets": [
            {
                "label": "Data Health Score",
                "data": [95, 94, 96, 93, 97, 95, 96]
            }
        ]
    }
