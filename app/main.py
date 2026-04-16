from fastapi import FastAPI

app = FastAPI(
    title="Service Monitor API",
    description="API para monitoramento da saude de serviços externos",
    version="1.0.0"
)

@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok"}