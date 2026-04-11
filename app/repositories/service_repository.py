from sqlalchemy.orm import Session
from app.models.service import Service
from app.schemas.service import ServiceCreate

class ServiceRepository:
    def create(self, db: Session, payload: ServiceCreate) -> Service:
        service = Service(**payload.model_dump())
        db.add(service)
        db.commit()
        db.refresh(service)
        
        return service

    def list_all(self, db: Session):
        return db.query(Service).all()
    
    def get_by_id(self, db: Session, service_id: int):
        return db.query(Service).filter(Service.id == service_id)