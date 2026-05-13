from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CheckResultResponse(BaseModel):
    id: int
    service_id: int
    status: int | None
    response_time_ms: int | None
    is_up: bool
    error_message: str | None
    checked_at: datetime

    model_config = ConfigDict(from_attributes=True)
