from fastapi import FastAPI
import requests
from .api import router

app = FastAPI(title="Item CRUD Service")

app.include_router(router)

ANALYTICS_SERVICE_URL = "http://localhost:8001"


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Item CRUD Service"}


@app.get("/analytics")
def get_analytics():
    try:
        response = requests.get(f"{ANALYTICS_SERVICE_URL}/api/v1/statistics", timeout=2)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": "Could not reach analytics service", "details": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
