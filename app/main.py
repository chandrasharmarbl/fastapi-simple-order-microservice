from fastapi import FastAPI
from app.api.items import router as items_router

app = FastAPI(title="FastAPI Microservice")

app.include_router(items_router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "fastapi-microservice"
    }
