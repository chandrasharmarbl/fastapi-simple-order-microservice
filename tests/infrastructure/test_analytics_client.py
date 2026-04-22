import pytest
from unittest.mock import patch, MagicMock
import httpx
from app.infrastructure.analytics_client import AsyncAnalyticsClient


@pytest.fixture
def analytics_client():
    return AsyncAnalyticsClient(base_url="http://test-analytics")


@pytest.mark.asyncio
async def test_log_event_success(analytics_client):
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        await analytics_client.log_event(
            operation="CREATE",
            item_id=1,
            item_name="Test Item",
            details="Test details"
        )
        
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert args[0] == "http://test-analytics/api/v1/log-event"
        assert "json" in kwargs
        assert kwargs["json"]["operation"] == "CREATE"
        assert kwargs["json"]["item_id"] == 1
        assert kwargs["json"]["item_name"] == "Test Item"
        assert kwargs["json"]["details"] == "Test details"
        assert "timestamp" in kwargs["json"]


@pytest.mark.asyncio
async def test_log_event_handles_exception_silently(analytics_client):
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_post.side_effect = httpx.RequestError("Network Error", request=MagicMock())
        
        # This should fail the test if an exception is raised
        # The design requires the analytics logger to fail silently
        await analytics_client.log_event(
            operation="CREATE",
            item_id=1,
            item_name="Test Item"
        )
