import asyncio
from unittest.mock import AsyncMock

import pytest
from extensions.eda.plugins.event_source.nautobot_changelog import main as nautobot_main


@pytest.mark.asyncio
async def test_main_with_mocked_http_request():
    queue = asyncio.Queue()

    # Define the arguments (as would be passed into the main function)
    args = {
        "instance": "http://localhost:8080",
        "token": "0123456789abcdef0123456789abcdef01234567",
        "query": "",
        "interval": 5,
    }

    # Mock the HTTP response from the Nautobot API
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(
        return_value={
            "results": [
                {
                    "id": "1",
                    "object_data_v2": {"key": "value"},
                    "time": "2025-03-14T00:00:00.000000Z",
                },
                {
                    "id": "2",
                    "object_data_v2": {"key": "value2"},
                    "time": "2025-03-14T01:00:00.000000Z",
                },
            ]
        }
    )
    for record in mock_response.json.return_value["results"]:
        await queue.put(record["object_data_v2"])
    task = asyncio.create_task(nautobot_main(queue, args))
    asyncio.gather(task)
    event = await queue.get()
    assert event == {"key": "value"}
    event = await queue.get()
    assert event == {"key": "value2"}
    assert queue.empty()
    task.cancel()
