import logging
import sys
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Configure a simple standalone logger for the analytics service
logging.basicConfig(
    level=logging.INFO, 
    stream=sys.stdout, 
    format="%(asctime)s - ANALYTICS SERVICE - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Analytics Microservice")

class EventLog(BaseModel):
    operation: str
    item_id: int
    item_name: str
    timestamp: datetime
    details: Optional[str] = ""

# Simple in-memory storage for events
events_db = []

@app.post("/api/v1/log-event", status_code=201)
async def log_event(event: EventLog):
    events_db.append(event)
    logger.info(
        f"Event Received -> Operation: {event.operation} | "
        f"Item: {event.item_name} (ID: {event.item_id}) | "
        f"Details: {event.details}"
    )
    return {"status": "Event logged successfully"}

@app.get("/api/v1/statistics")
async def get_statistics():
    return {
        "total_events": len(events_db),
        "events": events_db
    }
