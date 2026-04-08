from pydantic import BaseModel
from datetime import datetime

class CheckResultResponse(BaseModel):
    id: int
    service_id: int
    status: int | None
    response_time_ms: int | None
    is_up: bool
    error_message: str | None
    checked_at: datetime

    class Config:
        from_attributes = True