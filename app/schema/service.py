from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


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

    model_config = ConfigDict(from_attributes=True)
