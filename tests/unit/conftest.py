"""Pytest conftest setup."""
import pytest
import pynautobot

try:
    from plugins.module_utils.utils import NautobotApiBase
except ImportError:
    import sys

    sys.path.append("tests/")
    sys.path.append("plugins/module_utils")
    from utils import NautobotApiBase


@pytest.fixture(autouse=True)
def patch_pynautobot_version_check(monkeypatch):
    monkeypatch.setattr(pynautobot.api, "version", "2.0")


@pytest.fixture
def nautobot_api_base():
    return NautobotApiBase(url="https://nautobot.mock.com", token="abc123", valdiate_certs=False)


@pytest.fixture
def graphql_test_query():
    return """
query {
  sites {
    name
  }
}
"""


@pytest.fixture
def graphql_test_variables():
    return {"site_name": "DEN"}


@pytest.fixture
def graphql_test_query_with_var():
    return """
query() {
  sites {
    name
  }
}
"""


@pytest.fixture
def nautobot_url():
    return "https://nautobot.example.com"


@pytest.fixture
def nautobot_valid_args(graphql_test_query):
    return {
        "url": "https://nautobot.example.com",
        "token": "abc123",
        "validate_certs": False,
        "query": graphql_test_query,
        "graph_variables": {},
        "update_hostvars": False,
    }
