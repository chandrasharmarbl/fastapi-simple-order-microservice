from pydantic import BaseModel


class Event(BaseModel):
    operation: str
    item_id: int
    item_name: str
    timestamp: str
    details: str
