from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
import json
import os
from functools import partial
from unittest.mock import patch, MagicMock, Mock, call
from ansible.inventory.data import InventoryData

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
def expected_groups_dot_notation():
    return ["all", "ungrouped", "nautobot_airports", "nautobot_baseball_stadiums"]


@pytest.fixture
def expected_groups_backwards_compatability_site():
    return ["all", "ungrouped", "ATL01", "AMS01", "ANG01", "ATL02"]


@pytest.fixture
def inventory_fixture():
    inventory = InventoryModule()
    inventory.inventory = InventoryData()

    return inventory


def test_group_by_path(inventory_fixture, expected_groups_dot_notation):
    json_data = load_relative_test_data("graphql_groups")
    inventory_fixture.group_by = ["tenant.slug"]
    inventory_fixture.create_groups(json_data)
    inventory_groups = list(inventory_fixture.inventory.groups.keys())
    print(inventory_fixture.inventory.get_groups_dict())
    assert expected_groups_dot_notation == inventory_groups


def test_group_by_backwards_compatability(inventory_fixture, expected_groups_backwards_compatability_site):
    json_data = load_relative_test_data("graphql_groups")
    inventory_fixture.group_by = ["site"]
    inventory_fixture.create_groups(json_data)
    inventory_groups = list(inventory_fixture.inventory.groups.keys())
    assert expected_groups_backwards_compatability_site == inventory_groups
