"""Tests for Nautobot Query Lookup Plugin."""

from ansible.errors import AnsibleError, AnsibleLookupError
import pytest
from unittest.mock import patch, MagicMock


try:
    from plugins.lookup.lookup import LookupModule
except ImportError:
    import sys

    sys.path.append("tests")
    sys.path.append("plugins/lookup")

    from lookup import LookupModule


@pytest.fixture
def lookup():
    """Fixture to create an instance of your lookup plugin."""
    return LookupModule()


@patch("plugins.lookup.lookup.pynautobot.api")
def test_basic_run(mock_pynautobot, lookup):
    """Test basic functionality of the run method."""
    mock_api = MagicMock()
    mock_pynautobot.return_value = mock_api
    mock_api.dcim.devices.all.return_value = [{"id": 1, "name": "device1"}]

    terms = ["devices"]
    kwargs = {
        "token": "fake-token",
        "api_endpoint": "https://nautobot.local",
    }
    result = lookup.run(terms, **kwargs)

    mock_pynautobot.assert_called_once_with("https://nautobot.local", token="fake-token", api_version=None, verify=True, retries="0")
    assert result == [{"key": 1, "value": {"id": 1, "name": "device1"}}], "Expected a successful result"


def test_invalid_terms(lookup):
    """Test when terms is not a list or valid input."""
    with pytest.raises(AnsibleError, match="Unrecognised term"):
        with patch("plugins.lookup.lookup.get_endpoint", side_effect=KeyError):
            kwargs = {
                "token": "fake-token",
                "api_endpoint": "https://nautobot.local",
            }
            lookup.run("invalid.term", **kwargs)


@patch("plugins.lookup.lookup.pynautobot.api")
def test_no_token_or_endpoint(mock_pynautobot, lookup):
    """Test when neither token nor endpoint is provided."""
    with pytest.raises(AnsibleError):
        lookup.run(["devices"], token=None, api_endpoint=None)
