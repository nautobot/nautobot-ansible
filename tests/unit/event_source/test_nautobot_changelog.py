import asyncio
from unittest.mock import AsyncMock, patch

import pytest
from extensions.eda.plugins.event_source.nautobot_changelog import main as nautobot_main


@pytest.mark.asyncio
async def test_main():
    queue = asyncio.Queue()
    args = {
        "instance": "http://localhost:8080",
        "token": "0123456789abcdef0123456789abcdef01234567",
        "query": "",
        "interval": 1,
    }

    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(
        return_value={
            "results": [
                {
                    "time": "2023-02-22T03:07:51.453470Z",
                    "id": "1",
                    "object_data": {"key": "value"},
                },
                {
                    "time": "2023-02-22T03:07:52.453470Z",
                    "id": "2",
                    "object_data": {"key": "value2"},
                },
            ]
        }
    )

    with patch("aiohttp.ClientSession.get", return_value=mock_response):
        with patch("time.time", return_value=1677020871.453470):
            with patch("time.strftime", return_value="2023-02-22 03:07:51"):
                task = asyncio.create_task(nautobot_main(queue, args))
                await asyncio.sleep(2)
                task.cancel()
                await queue.put({"key": "value"})
                assert not queue.empty()
                event = await queue.get()
                assert event == {"key": "value"}
