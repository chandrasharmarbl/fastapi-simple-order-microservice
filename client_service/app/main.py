from fastapi import FastAPI
from .api import router

app = FastAPI(title="Order Service")

app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Order Service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
