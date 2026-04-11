from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import engine, Base
from app.schemas.service import ServiceCreate, ServiceResponse
from app.schemas.check_result import CheckResultResponse
from app.repositories.service_repository import ServiceRepository
from app.repositories.check_result_repository import CheckResultRepository
from app.services.monitor_service import MonitorService
from api.dependencies import get_db

Base.metadata.create_all(bind=engine)

router = APIRouter()
service_repository = ServiceRepository()
check_result_repository = CheckResultRepository()
monitor_service = MonitorService()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/services", response_model=ServiceResponse)
def create_service(payload: ServiceCreate, db: Session = Depends(get_db)):
    return service_repository.create(db, payload)

@router.get("/services", response_model=list[ServiceResponse])
def list_services(db: Session = Depends(get_db)):
    return service_repository.list_all(db)

@router.post("/services/{service_id}/check", response_model=CheckResultResponse)
async def check_service(service_id: int, db: Session = Depends(get_db)):
    result = await monitor_service.run_check(db, service_id)

    if not result:
        raise HTTPException(status_code=404, detail="Service not found")

    return result

@router.get("/services/{service_id}/history", response_model=list[CheckResultResponse])
def get_history(service_id: int, db: Session = Depends(get_db)):
    return check_result_repository.list_by_service(db, service_id)