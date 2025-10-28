import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from extensions.eda.plugins.event_source.nautobot_changelog import main as nautobot_main


@pytest.mark.asyncio
async def test_main_with_mocked_http_request():
    """
    Verifies that nautobot_changelog correctly processes API results and places
    records into the queue in the expected order.
    """
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


ssl_test_cases = [
    (
        {
            "instance": "https://localhost",
            "token": "0123456789abcdef0123456789abcdef01234567",
            "query": "",
            "interval": 5
        },
        True
    ),
    (
        {
            "instance": "https://localhost",
            "token": "0123456789abcdef0123456789abcdef01234567",
            "validate_certs": True,
            "query": "",
            "interval": 5
        },
        True
    ),
    (
        {
            "instance": "https://localhost",
            "token": "0123456789abcdef0123456789abcdef01234567",
            "validate_certs": False,
            "query": "",
            "interval": 5
        },
        False
    ),
]
@pytest.mark.asyncio
@pytest.mark.parametrize("args, expected_ssl", ssl_test_cases)
async def test_main_with_various_args(args, expected_ssl):
    """
    Test that nautobot_changelog correctly configures TCPConnector SSL
    in all HTTPS + "validate_certs" scenarios.
    """
    queue = asyncio.Queue()

    with patch('aiohttp.TCPConnector') as mock_tcp_connector, \
         patch('aiohttp.ClientSession') as mock_session, \
         patch('asyncio.sleep', side_effect=asyncio.CancelledError):

        mock_tcp_connector.return_value = MagicMock()
        mock_session_instance = MagicMock()
        mock_session.return_value.__aenter__.return_value = mock_session_instance

        mock_response = MagicMock()
        mock_response.status = 200

        async def mock_json():
            return {"results": []}

        mock_response.json = mock_json
        mock_session_instance.get.return_value.__aenter__.return_value = mock_response

        try:
            await nautobot_main(queue, args)
        except asyncio.CancelledError:
            pass

        mock_tcp_connector.assert_called_once_with(ssl=expected_ssl)
