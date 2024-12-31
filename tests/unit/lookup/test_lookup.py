"""Tests for Nautobot Query Lookup Plugin."""

from ansible.errors import AnsibleError
from ansible.template import Templar
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
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


@patch("plugins.lookup.lookup.pynautobot.api")
def test_run_with_static_filter(mock_pynautobot, lookup):
    """Test filters functionality of the run method."""
    mock_api = MagicMock()
    mock_pynautobot.return_value = mock_api
    mock_api.dcim.devices.filter.return_value = [{"id": 1, "name": "device1"}]

    # Initialize Ansible's Templar with necessary components
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=[])
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    templar = Templar(loader=loader, variables=variable_manager.get_vars())
    lookup._templar = templar

    terms = ["devices"]
    kwargs = {
        "token": "fake-token",
        "api_endpoint": "https://nautobot.local",
        "api_filter": "{'name': 'device1'}",
    }
    result = lookup.run(terms, **kwargs)

    mock_pynautobot.assert_called_once_with("https://nautobot.local", token="fake-token", api_version=None, verify=True, retries="0")
    mock_api.dcim.devices.filter.assert_called_once_with(_raw_params=["{'name':", "'device1'}"])
    assert result == [{"key": 1, "value": {"id": 1, "name": "device1"}}], "Expected a successful result"


@patch("plugins.lookup.lookup.pynautobot.api")
def test_run_with_dynamic_filter(mock_pynautobot, lookup):
    """Test dynamic filters functionality of the run method."""
    mock_api = MagicMock()
    mock_pynautobot.return_value = mock_api
    mock_api.dcim.devices.filter.return_value = [{"id": 1, "name": "device1"}]

    # Initialize Ansible's Templar with necessary components
    loader = DataLoader()
    variables = {"device_name": "device1"}
    templar = Templar(loader=loader, variables=variables)
    lookup._templar = templar

    terms = ["devices"]
    kwargs = {
        "token": "fake-token",
        "api_endpoint": "https://nautobot.local",
        "api_filter": "{'name': '{{ device_name }}'}",
    }
    result = lookup.run(terms, **kwargs)

    mock_pynautobot.assert_called_once_with("https://nautobot.local", token="fake-token", api_version=None, verify=True, retries="0")
    mock_api.dcim.devices.filter.assert_called_once_with(_raw_params=["{'name':", "'device1'}"])
    assert result == [{"key": 1, "value": {"id": 1, "name": "device1"}}], "Expected a successful result"
