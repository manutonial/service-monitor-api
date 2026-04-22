from sqlalchemy.orm import Session
from app.models.check_result import CheckResult

class CheckResultRepository:
    def create(self, db: Session, **fields): 
        check = CheckResult(**fields)
        db.add(check)
        db.commit()
        db.refresh(check)

        return check
    
    def list_by_service(self, db: Session, service_id: int):
        return db.query(CheckResult).filter(CheckResult.service_id == service_id).all()