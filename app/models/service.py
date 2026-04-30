
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)
    expected_status = Column(Integer, default=200)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    checks = relationship(
        "CheckResult",
        back_populates="service",
        cascade="all, delete-orphan",
    )