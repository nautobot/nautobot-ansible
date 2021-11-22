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
from netutils.lib_mapper import ANSIBLE_LIB_MAPPER_REVERSE, NAPALM_LIB_MAPPER

try:
    from ansible_collections.networktocode.nautobot.plugins.inventory.gql_inventory import InventoryModule

except ImportError:
    import sys

    # Not installed as a collection
    # Try importing relative to root directory of this ansible_modules project

    sys.path.append("plugins/inventory/")
    sys.path.append("tests")
    from gql_inventory import InventoryModule


def load_graphql_device_data(path, test_path):
    with open(f"{path}/test_data/{test_path}/device_data.json", "r") as f:
        data = json.loads(f.read())
    return data


load_relative_test_data = partial(load_graphql_device_data, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def inventory_fixture():
    inventory = InventoryModule()
    inventory.inventory = InventoryData()
    inventory.inventory.add_host("mydevice")

    return inventory


@pytest.fixture
def device_data():
    json_data = load_relative_test_data("graphql_groups")
    return json_data


def test_group_by_path_multiple(inventory_fixture, device_data):
    inventory_fixture.group_by = ["device_role.color_category.primary"]
    inventory_fixture.create_groups(device_data)
    inventory_groups = list(inventory_fixture.inventory.groups.keys())
    local_device_type_inventory_hosts = inventory_fixture.inventory.get_groups_dict().get("red")
    assert ["all", "ungrouped", "red"] == inventory_groups
    assert ["mydevice"] == local_device_type_inventory_hosts


def test_group_by_path(inventory_fixture, device_data):
    inventory_fixture.group_by = ["tenant.type"]
    inventory_fixture.create_groups(device_data)
    inventory_groups = list(inventory_fixture.inventory.groups.keys())
    local_device_type_inventory_hosts = inventory_fixture.inventory.get_groups_dict().get("local")
    assert ["all", "ungrouped", "local"] == inventory_groups
    assert ["mydevice"] == local_device_type_inventory_hosts


def test_group_by_string_only(inventory_fixture, device_data):
    inventory_fixture.group_by = ["site"]
    inventory_fixture.create_groups(device_data)
    inventory_groups = list(inventory_fixture.inventory.groups.keys())
    atl01_inventory_hosts = inventory_fixture.inventory.get_groups_dict().get("ATL01")
    assert ["all", "ungrouped", "ATL01"] == inventory_groups
    assert ["mydevice"] == atl01_inventory_hosts


@patch.object(Display, "display")
def test_no_parent_value(mock_display, inventory_fixture, device_data):
    inventory_fixture.group_by = ["color.slug"]
    inventory_fixture.create_groups(device_data)
    mock_display.assert_any_call("Could not find value for color on device mydevice")


@patch.object(Display, "display")
def test_multiple_group_by_one_fail(mock_display, inventory_fixture, device_data):
    inventory_fixture.group_by = ["color.slug", "site.name"]
    inventory_fixture.create_groups(device_data)
    inventory_groups = list(inventory_fixture.inventory.groups.keys())
    atl01_inventory_hosts = inventory_fixture.inventory.get_groups_dict().get("ATL01")
    mock_display.assert_any_call("Could not find value for color on device mydevice")
    assert ["all", "ungrouped", "ATL01"] == inventory_groups
    assert ["mydevice"] == atl01_inventory_hosts


def test_multiple_group_by_no_fail(inventory_fixture, device_data):
    inventory_fixture.group_by = ["status.name", "site.name"]
    inventory_fixture.create_groups(device_data)
    inventory_groups = list(inventory_fixture.inventory.groups.keys())
    atl01_inventory_hosts = inventory_fixture.inventory.get_groups_dict().get("ATL01")
    active_inventory_hosts = inventory_fixture.inventory.get_groups_dict().get("Active")
    assert ["all", "ungrouped", "Active", "ATL01"] == inventory_groups
    assert ["mydevice"] == atl01_inventory_hosts
    assert ["mydevice"] == active_inventory_hosts


@patch.object(Display, "display")
def test_no_chain_value(mock_display, inventory_fixture, device_data):
    inventory_fixture.group_by = ["site.type"]
    inventory_fixture.create_groups(device_data)
    mock_display.assert_any_call("Could not find value for type in site.type on device mydevice")


@patch.object(Display, "display")
def test_no_name_or_slug_value(mock_display, inventory_fixture, device_data):
    inventory_fixture.group_by = ["platform"]
    inventory_fixture.create_groups(device_data)
    mock_display.assert_any_call("No slug or name value for {'napalm_driver': 'asa'} in platform on device mydevice.")


@patch.object(Display, "display")
def test_group_name_dict(mock_display, inventory_fixture, device_data):
    inventory_fixture.group_by = ["platform"]
    inventory_fixture.create_groups(device_data)
    mock_display.assert_any_call("No slug or name value for {'napalm_driver': 'asa'} in platform on device mydevice.")


def test_add_ipv4(inventory_fixture, device_data):
    inventory_fixture.group_by = ["site"]
    inventory_fixture.create_groups(device_data)
    inventory_fixture.add_ipv4_address(device_data)
    mydevice_host = inventory_fixture.inventory.get_host("mydevice")
    assert mydevice_host.vars.get("ansible_host") == "10.10.10.10/32"


def test_ansible_platform(inventory_fixture, device_data):
    inventory_fixture.group_by = ["site"]
    inventory_fixture.create_groups(device_data)
    inventory_fixture.add_ansible_platform(device_data)
    mydevice_host = inventory_fixture.inventory.get_host("mydevice")
    assert mydevice_host.vars.get("ansible_network_os") == "cisco.asa.asa"
