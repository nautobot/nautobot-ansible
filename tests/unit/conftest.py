"""Pytest conftest setup."""
import pytest

from plugins.module_utils.utils import NautobotApiBase

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
    return {"site_name": "den"}


@pytest.fixture
def graphql_test_query_with_var():
    return """
query() {
  sites {
    name
  }
}
"""
