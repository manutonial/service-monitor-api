from fastapi import FastAPI

app = FastAPI(
    title="Service Monitor API",
    description="Api for health check third party services",
    version="1.0.0"
)

@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok"}