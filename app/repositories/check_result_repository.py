from sqlalchemy.orm import Session

from app.models.check_result import CheckResult


class CheckResultRepository:
    def create(self, db: Session, **fields):
        check = CheckResult(**fields)
        db.add(check)
        db.commit()
        db.refresh(check)

        return check

    def list_by_service(self, db: Session, service_id: int, limit: int = 5):
        return (
            db.query(CheckResult)
            .filter(CheckResult.service_id == service_id)
            .order_by(CheckResult.checked_at.desc())
            .limit(limit)
            .all()
        )
