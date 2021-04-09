"""Tests for Nautobot GraphQL Query Lookup Plugin."""
from ansible.errors import AnsibleError, AnsibleLookupError
import pynautobot
import pytest

from plugins.lookup.lookup_graphql import nautobot_lookup_graphql


def test_setup_api_error_missing_url():
    with pytest.raises(AnsibleLookupError) as exc:
        test_class = nautobot_lookup_graphql(token="abc123", validate_certs=False)

    assert str(exc.value) == "Missing URL of Nautobot"


def test_setup_api_error_incorrect_validate_certs():
    with pytest.raises(AnsibleLookupError) as exc:
        test_class = nautobot_lookup_graphql(
            url="https://nautobot.example.com", token="abc123", validate_certs="Hi"
        )

    assert str(exc.value) == "validate_certs must be a boolean"


def test_query_api_query_error_none(nautobot_url):
    with pytest.raises(AnsibleError) as exc:
        test_class = nautobot_lookup_graphql(
            url=nautobot_url,
            token="abc123",
            validate_certs=False,
            query=None,
            variables=None,
        )

    assert (
        str(exc.value)
        == "Query parameter was not passed. Please verify that query is passed."
    )


def test_query_api_query_error_dictionary(nautobot_url):
    with pytest.raises(AnsibleError) as exc:
        test_class = nautobot_lookup_graphql(
            url=nautobot_url,
            token="abc123",
            validate_certs=False,
            query={"ntc": "networktocode"},
            variables=None,
        )

    assert (
        str(exc.value)
        == "Query parameter must be of type string. Please see docs for examples."
    )


def test_query_api_query_variables_wrong_type(
    graphql_test_query_with_var, nautobot_url
):
    with pytest.raises(AnsibleError) as exc:
        test_class = nautobot_lookup_graphql(
            url=nautobot_url,
            token="abc123",
            validate_certs=False,
            query=graphql_test_query_with_var,
            variables=["ntc"],
        )

    assert (
        str(exc.value)
        == "Variables parameter must be of key/value pairs. Please see docs for examples."
    )
