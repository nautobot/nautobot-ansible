from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
import json
import os

from functools import partial
from unittest.mock import patch, MagicMock, Mock, call
from ansible.inventory.data import InventoryData
from ansible.errors import AnsibleError
from ansible.utils.display import Display

try:
    from ansible_collections.networktocode.nautobot.plugins.inventory.gql_inventory import InventoryModule

except ImportError:
    import sys

    # Not installed as a collection
    # Try importing relative to root directory of this ansible_modules project

    sys.path.append("plugins/inventory/")
    sys.path.append("tests")
    from gql_inventory import InventoryModule


def load_graphql_test_data(path, test_path):
    with open(f"{path}/test_data/{test_path}/data.json", "r") as f:
        data = json.loads(f.read())
    return data


load_relative_test_data = partial(load_graphql_test_data, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def active_status_expected_hosts():
    return [
        "aaa00-descriptor-01",
        "ams01-edge-01",
        "ams01-edge-02",
        "ams01-leaf-01",
        "ams01-leaf-02",
        "ams01-leaf-03",
        "ams01-leaf-04",
        "ams01-leaf-05",
        "ams01-leaf-06",
        "ams01-leaf-07",
        "ams01-leaf-08",
        "ang01-edge-01",
        "ang01-edge-02",
        "ang01-leaf-01",
        "ang01-leaf-02",
        "ang01-leaf-03",
        "ang01-leaf-04",
        "atl01-edge-01",
        "atl01-edge-02",
        "atl01-leaf-01",
        "atl01-leaf-02",
        "atl01-leaf-03",
        "atl01-leaf-04",
        "atl01-leaf-05",
        "atl01-leaf-06",
        "atl01-leaf-07",
        "atl01-leaf-08",
        "atl02-edge-01",
        "atl02-edge-02",
        "atl02-leaf-01",
    ]


@pytest.fixture
def expected_groups_status_name():
    return ["all", "ungrouped", "Active"]


@pytest.fixture
def expected_groups_site_string_only():
    return ["all", "ungrouped", "ATL01", "AMS01", "ANG01", "ATL02"]


@pytest.fixture()
def site_atl02_expected_hosts():
    return ["atl02-edge-01", "atl02-edge-02", "atl02-leaf-01"]


@pytest.fixture
def expected_groups_tenant_slug():
    return ["all", "ungrouped", "ATL01", "AMS01", "ANG01", "ATL02"]


@pytest.fixture
def inventory_fixture():
    inventory = InventoryModule()
    inventory.inventory = InventoryData()

    return inventory


def test_group_by_path(inventory_fixture, expected_groups_status_name, active_status_expected_hosts):
    json_data = load_relative_test_data("graphql_groups")
    inventory_fixture.group_by = ["status.name"]
    inventory_fixture.create_groups(json_data)
    inventory_groups = list(inventory_fixture.inventory.groups.keys())
    active_status_inventory_hosts = inventory_fixture.inventory.get_groups_dict().get("Active")
    assert active_status_expected_hosts == active_status_inventory_hosts
    assert expected_groups_status_name == inventory_groups


def test_group_by_string_only(inventory_fixture, expected_groups_site_string_only, site_atl02_expected_hosts):
    json_data = load_relative_test_data("graphql_groups")
    inventory_fixture.group_by = ["site"]
    inventory_fixture.create_groups(json_data)
    inventory_groups = list(inventory_fixture.inventory.groups.keys())
    atl02_inventory_hosts = inventory_fixture.inventory.get_groups_dict().get("ATL02")
    assert expected_groups_site_string_only == inventory_groups
    assert site_atl02_expected_hosts == atl02_inventory_hosts


@patch.object(Display, "display")
def test_no_initial_value(mock_display, inventory_fixture):
    json_data = load_relative_test_data("graphql_groups")
    inventory_fixture.group_by = ["color.slug"]
    inventory_fixture.create_groups(json_data)
    mock_display.assert_any_call("Could not find value for color on device aaa00-descriptor-01")


@patch.object(Display, "display")
def test_no_value_subsequent_key(mock_display, inventory_fixture):
    json_data = load_relative_test_data("graphql_groups")
    inventory_fixture.group_by = ["site.rainbow"]
    inventory_fixture.create_groups(json_data)
    mock_display.assert_any_call("Could not find value for rainbow in site.rainbow on device aaa00-descriptor-01")
