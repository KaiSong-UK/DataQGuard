from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from pydantic import BaseModel
from typing import List, Optional

from core.database import get_db
from models.models import Datasource

router = APIRouter()


class DatasourceCreate(BaseModel):
    name: str
    type: str  # postgresql, mysql, mongodb
    host: str
    port: int
    database: str
    username: str
    password: str
    ssl_mode: Optional[str] = "prefer"


class DatasourceResponse(BaseModel):
    id: int
    name: str
    type: str
    host: str
    port: int
    database: str
    username: str
    ssl_mode: str
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[DatasourceResponse])
async def list_datasources(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Datasource))
    datasources = result.scalars().all()
    return datasources


@router.post("/", response_model=DatasourceResponse)
async def create_datasource(
    request: DatasourceCreate,
    db: AsyncSession = Depends(get_db)
):
    ds = Datasource(
        name=request.name,
        type=request.type,
        host=request.host,
        port=request.port,
        database=request.database,
        username=request.username,
        password=request.password,
        ssl_mode=request.ssl_mode
    )
    db.add(ds)
    await db.commit()
    await db.refresh(ds)
    return ds


@router.get("/{datasource_id}", response_model=DatasourceResponse)
async def get_datasource(datasource_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Datasource).where(Datasource.id == datasource_id))
    ds = result.scalar_one_or_none()
    if not ds:
        raise HTTPException(status_code=404, detail="Datasource not found")
    return ds


@router.delete("/{datasource_id}")
async def delete_datasource(datasource_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(delete(Datasource).where(Datasource.id == datasource_id))
    await db.commit()
    return {"message": "Datasource deleted"}


@router.post("/{datasource_id}/test")
async def test_datasource_connection(datasource_id: int, db: AsyncSession = Depends(get_db)):
    # TODO: Implement actual connection test
    return {"status": "connected", "latency_ms": 12}
