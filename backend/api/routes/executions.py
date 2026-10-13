
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.models import RuleExecution

router = APIRouter()


@router.get("/")
async def list_executions(
    rule_id: int = None,
    status: str = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    query = select(RuleExecution)
    
    if rule_id:
        query = query.where(RuleExecution.rule_id == rule_id)
    if status:
        query = query.where(RuleExecution.status == status)
    
    query = query.order_by(RuleExecution.started_at.desc()).limit(limit)
    
    result = await db.execute(query)
    executions = result.scalars().all()
    return executions


@router.get("/{execution_id}")
async def get_execution(execution_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RuleExecution).where(RuleExecution.id == execution_id)
    )
    execution = result.scalar_one_or_none()
    return execution
