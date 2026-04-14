import asyncio
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.celery_config import celery_app
from core.database import async_session
from models.models import Rule, RuleExecution, Datasource
from services.rule_engine import RuleEngine


@celery_app.task
def execute_rule_task(rule_id: int):
    """Execute a single rule"""
    asyncio.run(_execute_rule_async(rule_id))


async def _execute_rule_async(rule_id: int):
    async with async_session() as session:
        # Get rule
        result = await session.execute(select(Rule).where(Rule.id == rule_id))
        rule = result.scalar_one_or_none()
        
        if not rule or not rule.is_active:
            return
        
        # Create execution record
        execution = RuleExecution(
            rule_id=rule_id,
            status="running"
        )
        session.add(execution)
        await session.commit()
        await session.refresh(execution)
        
        try:
            # Get datasource
            result = await session.execute(
                select(Datasource).where(Datasource.id == rule.datasource_id)
            )
            datasource = result.scalar_one()
            
            # Execute rule
            engine = RuleEngine(datasource)
            result = await engine.execute_rule(rule)
            
            # Update execution
            execution.status = "success"
            execution.completed_at = datetime.utcnow()
            execution.total_rows = result.get("total_rows", 0)
            execution.failed_rows = result.get("failed_rows", 0)
            execution.pass_rate = result.get("pass_rate", 0.0)
            execution.details = result
            
        except Exception as e:
            execution.status = "failed"
            execution.completed_at = datetime.utcnow()
            execution.error_message = str(e)
        
        await session.commit()


@celery_app.task
def check_scheduled_rules():
    """Check and queue scheduled rules"""
    asyncio.run(_check_scheduled_rules_async())


async def _check_scheduled_rules_async():
    # TODO: Implement cron-based scheduling logic
    pass
