import httpx
import datetime
from app.domain.interfaces import AnalyticsClientProtocol
from app.core.logger import get_logger


logger = get_logger(__name__)

class AsyncAnalyticsClient(AnalyticsClientProtocol):
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def log_event(self, operation: str, item_id: int, item_name: str, details: str = "") -> None:
        event_data = {
            "operation": operation,
            "item_id": item_id,
            "item_name": item_name,
            "timestamp": datetime.datetime.now(datetime.UTC),
            "details": details,
        }
        
        # We instantiate a new client per request here for simplicity, 
        # but in a production app you'd ideally reuse the client across requests.
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/v1/log-event",
                    json=event_data,
                    timeout=2.0
                )
                response.raise_for_status()
            except httpx.RequestError as exc:
                logger.error(f"Analytics request failed: {exc}")
            except httpx.HTTPStatusError as exc:
                logger.error(f"Analytics responded with error status: {exc.response.status_code}")
