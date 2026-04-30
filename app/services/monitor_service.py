from sqlalchemy.orm import Session

from app.repositories.check_result_repository import CheckResultRepository
from app.repositories.service_repository import ServiceRepository
from app.services.http_checker import HttpChecker


class MonitorService:
    def __init__(self):
        self.service_repository = ServiceRepository()
        self.check_result_repository = CheckResultRepository()
        self.http_checker = HttpChecker()

    async def run_check(self, db: Session, service_id: int):
        service = self.service_repository.get_by_id(db, service_id)
        if not service:
            return None # route give status 404
        
        result = await self.http_checker.check(service.url)
        
        is_up = result["status"] is not None and result["status"] is service.expected_status
        
        return self.check_result_repository.create(
            db,
            service_id=service_id,
            status=result["status"],
            response_time_ms=result["response_time_ms"],
            is_up=is_up,
            error_message=result["error_message"],
        )