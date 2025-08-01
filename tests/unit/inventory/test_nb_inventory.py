# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Hillsong, Douglas Heriot (@DouglasHeriot) <douglas.heriot@hillsong.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
from functools import partial
from unittest.mock import Mock, call

import pytest

try:
    from ansible_collections.networktocode.nautobot.plugins.inventory.inventory import InventoryModule
    from ansible_collections.networktocode.nautobot.tests.test_data import load_test_data

except ImportError:
    import sys

    # Not installed as a collection
    # Try importing relative to root directory of this ansible_modules project

    sys.path.append("plugins/inventory")
    sys.path.append("tests")
    from test_data import load_test_data

load_relative_test_data = partial(load_test_data, os.path.dirname(os.path.abspath(__file__)))


class MockInventory:
    def __init__(self):
        self.variables = {}

    def set_variable(self, hostname, key, value):
        if hostname not in self.variables:
            self.variables[hostname] = {}

        self.variables[hostname][key] = value


@pytest.fixture
def inventory_fixture(allowed_device_query_parameters_fixture, allowed_vm_query_parameters_fixture):
    inventory = InventoryModule()
    inventory.api_endpoint = "https://nautobot.test.endpoint:1234"

    # Fill in data that is fetched dynamically
    inventory.api_version = None
    inventory.allowed_device_query_parameters = allowed_device_query_parameters_fixture
    inventory.allowed_vm_query_parameters = allowed_vm_query_parameters_fixture
    # Inventory mock, to validate what has been set via inventory.inventory.set_variable
    inventory.inventory = MockInventory()
    inventory.wrap_variables = True

    return inventory


@pytest.fixture
def allowed_device_query_parameters_fixture():
    # Subset of parameters - real list is fetched dynamically from Nautobot openapi endpoint
    return [
        "id",
        "interfaces",
        "has_primary_ip",
        "location",
        "mac_address",
        "name",
        "platform",
        "rack_id",
        "role",
        "tag",
    ]


@pytest.fixture
def allowed_vm_query_parameters_fixture():
    # Subset of parameters - real list is fetched dynamically from Nautobot openapi endpoint
    return [
        "id",
        "cluster",
        "interfaces",
        "disk",
        "mac_address",
        "has_primary_ip",
        "name",
        "platform",
        "role",
        "tag",
    ]


@pytest.mark.parametrize("parameter, expected", load_relative_test_data("validate_query_parameter"))
def test_validate_query_parameter(inventory_fixture, parameter, expected):
    value = "some value, doesn't matter"
    result = inventory_fixture.validate_query_parameter(
        {parameter: value}, inventory_fixture.allowed_device_query_parameters
    )
    assert (result == (parameter, value)) == expected


@pytest.mark.parametrize("parameters, expected", load_relative_test_data("filter_query_parameters"))
def test_filter_query_parameters(inventory_fixture, parameters, expected):
    result = inventory_fixture.filter_query_parameters(parameters, inventory_fixture.allowed_device_query_parameters)

    # Result is iterators of tuples
    # expected from json file is an array of dicts

    # Convert result iterator to list so we can get the length, and iterate over with an index
    result_list = list(result)

    assert len(result_list) == len(expected)

    for i, parameter in enumerate(result_list):
        assert parameter[0] == list(expected[i].keys())[0]
        assert parameter[1] == list(expected[i].values())[0]


@pytest.mark.parametrize("options, expected", load_relative_test_data("refresh_url"))
def test_refresh_url(inventory_fixture, options, expected):
    inventory_fixture.query_filters = options["query_filters"]
    inventory_fixture.device_query_filters = options["device_query_filters"]
    inventory_fixture.vm_query_filters = options["vm_query_filters"]
    inventory_fixture.config_context = options["config_context"]

    result = inventory_fixture.refresh_url()

    assert result == tuple(expected)


@pytest.mark.filterwarnings("ignore:Exception")
def test_refresh_lookups(inventory_fixture):
    def raises_exception():
        raise Exception("Error from within a thread")

    def does_not_raise():
        pass

    with pytest.raises(Exception) as e:
        inventory_fixture.refresh_lookups([does_not_raise, raises_exception])
    assert "Error from within a thread" in str(e)

    inventory_fixture.refresh_lookups([does_not_raise, does_not_raise])


@pytest.mark.parametrize(
    "plurals, services, interfaces, dns_name, ansible_host_dns_name, expected, not_expected",
    load_relative_test_data("group_extractors"),
)
def test_group_extractors(
    inventory_fixture,
    plurals,
    services,
    interfaces,
    dns_name,
    ansible_host_dns_name,
    expected,
    not_expected,
):
    inventory_fixture.plurals = plurals
    inventory_fixture.services = services
    inventory_fixture.interfaces = interfaces
    inventory_fixture.dns_name = dns_name
    inventory_fixture.ansible_host_dns_name = ansible_host_dns_name
    extractors = inventory_fixture.group_extractors

    for key in expected:
        assert key in extractors

    for key in not_expected:
        assert key not in expected


@pytest.mark.parametrize(
    "api_url, max_uri_length, query_key, query_values, expected",
    load_relative_test_data("get_resource_list_chunked"),
)
def test_get_resource_list_chunked(inventory_fixture, api_url, max_uri_length, query_key, query_values, expected):
    mock_get_resource_list = Mock()
    mock_get_resource_list.return_value = ["resource"]

    inventory_fixture.get_resource_list = mock_get_resource_list
    inventory_fixture.max_uri_length = max_uri_length

    resources = inventory_fixture.get_resource_list_chunked(api_url, query_key, query_values)

    mock_get_resource_list.assert_has_calls(map(call, expected))
    assert mock_get_resource_list.call_count == len(expected)
    assert resources == mock_get_resource_list.return_value * len(expected)


def test_rename_variables(inventory_fixture):
    inventory_fixture.rename_variables = inventory_fixture.parse_rename_variables(
        (
            {"pattern": r"cluster(.*)", "repl": r"nautobot_cluster\1"},
            {"pattern": r"ansible_host", "repl": r"host"},
        )
    )

    inventory_fixture._set_variable("host", "ansible_fqdn", "host.example.org")
    inventory_fixture._set_variable("host", "ansible_host", "host")
    inventory_fixture._set_variable("host", "cluster", "staging")
    inventory_fixture._set_variable("host", "cluster_id", "0xdeadbeef")

    assert inventory_fixture.inventory.variables["host"] == {
        "ansible_fqdn": "host.example.org",
        "host": "host",
        "nautobot_cluster": "staging",
        "nautobot_cluster_id": "0xdeadbeef",
    }
