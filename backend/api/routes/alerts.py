from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from core.database import get_db
from models.models import Alert

router = APIRouter()


@router.get("/")
async def list_alerts(
    severity: str = None,
    is_sent: bool = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    query = select(Alert).order_by(Alert.created_at.desc())
    
    if severity:
        query = query.where(Alert.severity == severity)
    if is_sent is not None:
        query = query.where(Alert.is_sent == is_sent)
    
    query = query.limit(limit)
    
    result = await db.execute(query)
    alerts = result.scalars().all()
    return alerts


@router.post("/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int, db: AsyncSession = Depends(get_db)):
    # TODO: Implement acknowledgment
    return {"message": "Alert acknowledged"}
