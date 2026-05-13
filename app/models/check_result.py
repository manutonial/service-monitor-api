from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class CheckResult(Base):
    __tablename__ = "check_results"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, index=True)
    status = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    is_up = Column(Boolean, nullable=False)
    error_message = Column(String, nullable=True)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())

    service = relationship("Service", back_populates="checks")
