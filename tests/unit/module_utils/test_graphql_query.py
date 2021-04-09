"""Tests for Nautobot GraphQL Query Lookup Plugin."""
from ansible.errors import AnsibleError
import pynautobot
import pytest

from plugins.module_utils.utils import NautobotApiBase, NautobotGraphQL


def test_setup_api_base():
    test_class = NautobotApiBase(url="https://nautobot.example.com", token="abc123", validate_certs=False)
    assert isinstance(test_class.api, pynautobot.api)
    assert test_class.url == "https://nautobot.example.com"
    assert test_class.token == "abc123"
    assert test_class.ssl_verify == False


def test_setup_api_error_missing_url():
    with pytest.raises(AnsibleError) as exc:
        test_class = NautobotApiBase(token="abc123", validate_certs=False)

    assert str(exc.value) == "Missing URL of Nautobot"


def test_setup_api_error_incorrect_validate_certs():
    with pytest.raises(AnsibleError) as exc:
        test_class = NautobotApiBase(url="https://nautobot.example.com", token="abc123", validate_certs="Hi")
    
    assert str(exc.value) == "validate_certs must be a boolean"


def test_query_api_setup(nautobot_api_base, graphql_test_query):
    test_class = NautobotGraphQL(query=graphql_test_query, api=nautobot_api_base)
    assert isinstance(test_class, NautobotGraphQL)
    assert test_class.query == graphql_test_query
    assert isinstance(test_class.pynautobot.api, pynautobot.api)
    assert test_class.variables is None


def test_query_api_setup_with_variable(nautobot_api_base, graphql_test_query_with_var, graphql_test_variables):
    test_class = NautobotGraphQL(query=graphql_test_query_with_var, api=nautobot_api_base, variables=graphql_test_variables)
    assert isinstance(test_class, NautobotGraphQL)
    assert test_class.query == graphql_test_query_with_var
    assert isinstance(test_class.pynautobot.api, pynautobot.api)
    assert test_class.variables is graphql_test_variables


def test_query_api_query_error_none(nautobot_api_base):
    with pytest.raises(AnsibleError) as exc:
        test_class = NautobotGraphQL(query=None, api=nautobot_api_base, variables=None)

    assert str(exc.value) == "Query parameter was not passed. Please verify that query is passed."


def test_query_api_query_error_dictionary(nautobot_api_base):
    with pytest.raises(AnsibleError) as exc:
        test_class = NautobotGraphQL(query={"ntc": "networktocode"}, api=nautobot_api_base, variables=None)

    assert str(exc.value) == "Query parameter must be of type string. Please see docs for examples."


def test_query_api_query_variables_wrong_type(nautobot_api_base, graphql_test_query_with_var):
    with pytest.raises(AnsibleError) as exc:
        test_class = NautobotGraphQL(query=graphql_test_query_with_var, api=nautobot_api_base, variables=["ntc"])

    assert str(exc.value) == "Variables parameter must be of key/value pairs. Please see docs for examples."
