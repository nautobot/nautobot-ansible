"""Tests for Nautobot GraphQL filter plugins."""

import json

import pytest
from ansible_collections.networktocode.nautobot.plugins.filter.graphql import (
    build_graphql_filter_string,
    convert_to_graphql_string,
)


def load_test_data(test):
    with open(f"tests/unit/filter/test_data/{test}.json", "r") as f:
        data = json.loads(f.read())
    return data


@pytest.mark.parametrize(("test_data"), load_test_data("graphql_string"))
def test_convert_to_graphql_string(test_data):
    result = convert_to_graphql_string(test_data["query"])
    assert result == test_data["expected"]


def test_build_graphql_filter_string():
    gql_filters = {"role": "core", "$tenant": "den", "device_type": "c9300"}
    assert build_graphql_filter_string(gql_filters) == "(role: 'core', $tenant: den, device_type: 'c9300')"
