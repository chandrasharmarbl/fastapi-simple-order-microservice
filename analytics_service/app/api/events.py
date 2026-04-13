from fastapi import APIRouter
from typing import List
from ..models import Event

router = APIRouter(prefix="/api/v1", tags=["events"])

events_log = []


@router.post("/log-event")
def log_event(event: Event):
    events_log.append(event)
    return {"status": "logged", "event_count": len(events_log)}


@router.get("/events", response_model=List[Event])
def get_events():
    return events_log


@router.get("/statistics")
def get_statistics():
    operations = {}
    for event in events_log:
        op = event.operation
        operations[op] = operations.get(op, 0) + 1
    
    return {
        "total_events": len(events_log),
        "operations_breakdown": operations,
        "events": events_log
    }


@router.delete("/events")
def clear_events():
    global events_log
    events_log.clear()
    return {"status": "cleared"}
