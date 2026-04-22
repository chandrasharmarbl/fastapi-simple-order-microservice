from fastapi import FastAPI

app = FastAPI(title="FastAPI Microservice")


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "fastapi-microservice"
    }
