#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: inventory_item
short_description: Creates or removes inventory items from Nautobot
description:
  - Creates or removes inventory items from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  name:
    required: true
    type: str
  label:
    required: false
    type: str
  description:
    required: false
    type: str
  part_id:
    required: false
    type: str
  serial:
    required: false
    type: str
  asset_tag:
    required: false
    type: str
  discovered:
    required: false
    type: bool
  parent:
    required: false
    type: dict
  device:
    required: true
    type: dict
  manufacturer:
    required: false
    type: dict
  software_version:
    required: false
    type: dict
  software_image_files:
    required: false
    type: list
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create inventory_item within Nautobot with only required information
      networktocode.nautobot.inventory_item:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Inventory_Item
        device: None
        state: present

    - name: Delete inventory_item within nautobot
      networktocode.nautobot.inventory_item:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Inventory_Item
        state: absent
"""

RETURN = r"""
inventory_item:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import CUSTOM_FIELDS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import TAGS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_INVENTORY_ITEMS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            label=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            part_id=dict(required=False, type="str"),
            serial=dict(required=False, type="str"),
            asset_tag=dict(required=False, type="str"),
            discovered=dict(required=False, type="bool"),
            parent=dict(required=False, type="dict"),
            device=dict(required=True, type="dict"),
            manufacturer=dict(required=False, type="dict"),
            software_version=dict(required=False, type="dict"),
            software_image_files=dict(required=False, type="list"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    inventory_item = NautobotDcimModule(module, NB_INVENTORY_ITEMS)
    inventory_item.run()


if __name__ == "__main__":  # pragma: no cover
    main()
