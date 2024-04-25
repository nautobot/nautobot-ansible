"""Tests for Nautobot GraphQL Query Lookup Plugin."""

from ansible.errors import AnsibleError
import pynautobot
import pytest

try:
    from plugins.module_utils.utils import NautobotApiBase, NautobotGraphQL
except ImportError:
    import sys

    sys.path.append("plugins/module_utils")
    sys.path.append("tests")
    from utils import NautobotApiBase, NautobotGraphQL


def test_setup_api_base():
    test_class = NautobotApiBase(url="https://nautobot.example.com", token="abc123", ssl_verify=False)
    assert isinstance(test_class.api, pynautobot.api)
    assert test_class.url == "https://nautobot.example.com"
    assert test_class.token == "abc123"
    assert test_class.ssl_verify is False


def test_setup_api_base_ssl_verify_true():
    test_class = NautobotApiBase(url="https://nautobot.example.com", token="abc123", ssl_verify=True)
    assert isinstance(test_class.api, pynautobot.api)
    assert test_class.url == "https://nautobot.example.com"
    assert test_class.token == "abc123"
    assert test_class.ssl_verify is True


def test_query_api_setup(nautobot_api_base, graphql_test_query):
    test_class = NautobotGraphQL(query_str=graphql_test_query, api=nautobot_api_base)
    assert isinstance(test_class, NautobotGraphQL)
    assert test_class.query_str == graphql_test_query
    assert isinstance(test_class.pynautobot, pynautobot.api)
    assert test_class.variables is None


def test_query_api_setup_with_variable(nautobot_api_base, graphql_test_query_with_var, graphql_test_variables):
    test_class = NautobotGraphQL(
        query_str=graphql_test_query_with_var,
        api=nautobot_api_base,
        variables=graphql_test_variables,
    )
    assert isinstance(test_class, NautobotGraphQL)
    assert test_class.query_str == graphql_test_query_with_var
    assert isinstance(test_class.pynautobot, pynautobot.api)
    assert test_class.variables is graphql_test_variables
