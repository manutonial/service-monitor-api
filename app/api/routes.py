
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query, Session

from app.api.dependencies import get_db
from app.repositories.check_result_repository import CheckResultRepository
from app.repositories.service_repository import ServiceRepository
from app.schemas.check_result import CheckResultResponse
from app.schemas.service import ServiceCreate, ServiceResponse
from app.services.monitor_service import MonitorService

router = APIRouter()
service_repository = ServiceRepository()
check_result_repository = CheckResultRepository()
monitor_service = MonitorService()
    
@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/services", response_model=ServiceResponse, status_code=201)
def create_service(
    payload: ServiceCreate,
    db: Annotated[Session, Depends(get_db)]
):
    try:
        return service_repository.create(db, payload)
    # If the url already exists in the database, returns HTTPException
    except IntegrityError: 
        db.rollback
        raise HTTPException(status_code=409, detail="URL already has been created")

@router.get("/services", response_model=list[ServiceResponse])
def list_services(
    db: Annotated[Session, Depends(get_db)], 
    skip: int = Query(default=0), 
    limit: int = Query(default=100, le=500)
):
    return service_repository.list_all(db, skip=skip, limit=limit)

@router.post("/services/{service_id}/check", response_model=CheckResultResponse)
async def check_service(service_id: int, db: Annotated[Session, Depends(get_db)]):
    result = await monitor_service.run_check(db, service_id)
    if not result:
        raise HTTPException(status_code=404, detail="Service not found.")
    return result

@router.get("/services/{service_id}/history", response_model=list[CheckResultResponse])
def get_history(
    service_id: int,
    db: Annotated[Session, Depends(get_db)],
    limit: int = Query(default=50, ge=1, le=200)
):
    return check_result_repository.list_by_service(db, service_id, limit=limit)