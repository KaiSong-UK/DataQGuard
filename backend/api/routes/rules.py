from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from models.models import Rule, RuleExecution

router = APIRouter()


class RuleCreate(BaseModel):
    name: str
    description: str | None = None
    datasource_id: int
    table_name: str
    rule_type: str  # completeness, accuracy, consistency, timeliness, uniqueness
    rule_config: dict[str, Any]
    schedule: str = "0 */4 * * *"
    is_active: bool = True


class RuleResponse(BaseModel):
    id: int
    name: str
    description: str | None
    datasource_id: int
    table_name: str
    rule_type: str
    rule_config: dict[str, Any]
    schedule: str
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True


@router.get("/", response_model=list[RuleResponse])
async def list_rules(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rule))
    rules = result.scalars().all()
    return rules


@router.post("/", response_model=RuleResponse)
async def create_rule(request: RuleCreate, db: AsyncSession = Depends(get_db)):
    rule = Rule(
        name=request.name,
        description=request.description,
        datasource_id=request.datasource_id,
        table_name=request.table_name,
        rule_type=request.rule_type,
        rule_config=request.rule_config,
        schedule=request.schedule,
        is_active=request.is_active
    )
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule


@router.get("/{rule_id}", response_model=RuleResponse)
async def get_rule(rule_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rule).where(Rule.id == rule_id))
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.put("/{rule_id}", response_model=RuleResponse)
async def update_rule(rule_id: int, request: RuleCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rule).where(Rule.id == rule_id))
    rule = result.scalar_one_or_none()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    for key, value in request.dict().items():
        setattr(rule, key, value)
    
    await db.commit()
    await db.refresh(rule)
    return rule


@router.delete("/{rule_id}")
async def delete_rule(rule_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(delete(Rule).where(Rule.id == rule_id))
    await db.commit()
    return {"message": "Rule deleted"}


@router.post("/{rule_id}/execute")
async def execute_rule(rule_id: int, db: AsyncSession = Depends(get_db)):
    # TODO: Trigger Celery task
    execution = RuleExecution(
        rule_id=rule_id,
        status="pending"
    )
    db.add(execution)
    await db.commit()
    await db.refresh(execution)
    return {"message": "Rule execution queued", "execution_id": execution.id}


@router.get("/{rule_id}/executions")
async def get_rule_executions(rule_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RuleExecution).where(RuleExecution.rule_id == rule_id).order_by(RuleExecution.started_at.desc())
    )
    executions = result.scalars().all()
    return executions
