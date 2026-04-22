from fastapi import FastAPI
from app.api.routes import router
from app.core.database import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    lifespan=lifespan,
    title="Service Monitor API",
    description="Api for health check third party services",
    version="1.0.0"
)
app.include_router(router, prefix="/api/v1")

@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok"}