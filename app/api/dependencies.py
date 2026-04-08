from sqlalchemy.orm import Session
from app.core.database import SessionLocal

def get_db() -> Session: # type: ignore
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()