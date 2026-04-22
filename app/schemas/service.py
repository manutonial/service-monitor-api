from pydantic import BaseModel, HttpUrl
from datetime import datetime

class ServiceCreate(BaseModel):
    name: str
    url: HttpUrl
    expected_status: int = 200

class ServiceResponse(BaseModel):
    id: int
    name: str
    url: str
    expected_status: int
    created_at: datetime

    class Config:
        from_attributes = True