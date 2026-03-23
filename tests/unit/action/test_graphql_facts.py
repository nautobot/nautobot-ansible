"""Tests for Nautobot GraphQL Facts Action Plugin."""

import pytest
from ansible.errors import AnsibleError

try:
    from plugins.action.graphql_facts import nautobot_action_graphql_facts
except ImportError:
    import sys

    sys.path.append("tests")
    sys.path.append("plugins/action")

    from graphql_facts import nautobot_action_graphql_facts


def test_setup_api_error_missing_url(nautobot_valid_args):
    args = nautobot_valid_args
    args.pop("url")
    with pytest.raises(AnsibleError) as exc:
        test_class = nautobot_action_graphql_facts(args)

    assert str(exc.value) == "Missing URL of Nautobot"


def test_setup_api_error_incorrect_validate_certs(nautobot_valid_args):
    nautobot_valid_args["validate_certs"] = "Hi"
    with pytest.raises(AnsibleError) as exc:
        test_class = nautobot_action_graphql_facts(args=nautobot_valid_args)

    assert str(exc.value) == "validate_certs must be a boolean"


def test_query_api_query_error_none(nautobot_valid_args):
    nautobot_valid_args["query"] = None
    with pytest.raises(AnsibleError) as exc:
        test_class = nautobot_action_graphql_facts(args=nautobot_valid_args)

    assert str(exc.value) == "Query parameter was not passed. Please verify that query is passed."


def test_query_api_query_error_dictionary(nautobot_valid_args):
    nautobot_valid_args["query"] = {"ntc": "networktocode"}
    with pytest.raises(AnsibleError) as exc:
        test_class = nautobot_action_graphql_facts(args=nautobot_valid_args)

    assert str(exc.value) == "Query parameter must be of type string. Please see docs for examples."


def test_query_api_query_variables_wrong_type(nautobot_valid_args, graphql_test_query_with_var):
    nautobot_valid_args["query"] = graphql_test_query_with_var
    nautobot_valid_args["graph_variables"] = ["ntc"]
    with pytest.raises(AnsibleError) as exc:
        test_result = nautobot_action_graphql_facts(args=nautobot_valid_args)

    assert str(exc.value) == "graph_variables parameter must be of key/value pairs. Please see docs for examples."
