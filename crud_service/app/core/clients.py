import requests


ANALYTICS_SERVICE_URL = "http://localhost:8001"


def log_to_analytics(operation: str, item_id: int, item_name: str, details: str = ""):
    try:
        from datetime import datetime
        event_data = {
            "operation": operation,
            "item_id": item_id,
            "item_name": item_name,
            "timestamp": datetime.now().isoformat(),
            "details": details,
        }
        response = requests.post(
            f"{ANALYTICS_SERVICE_URL}/api/v1/log-event",
            json=event_data,
            timeout=2
        )
        response.raise_for_status()
    except requests.exceptions.RequestException:
        pass
