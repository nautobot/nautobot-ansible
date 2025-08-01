#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Mikhail Yohman (@FragmentedPacket)
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
  - Mikhail Yohman (@FragmentedPacket)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  device:
    description:
      - Name of the device the inventory item belongs to
      - Required if I(state=present) and the inventory item does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - Name of the inventory item to be created
      - Required if I(state=present) and the inventory item does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  manufacturer:
    description:
      - The manufacturer of the inventory item
    required: false
    type: raw
    version_added: "3.0.0"
  part_id:
    description:
      - The part ID of the inventory item
    required: false
    type: str
    version_added: "3.0.0"
  serial:
    description:
      - The serial number of the inventory item
    required: false
    type: str
    version_added: "3.0.0"
  asset_tag:
    description:
      - The asset tag of the inventory item
    required: false
    type: str
    version_added: "3.0.0"
  description:
    description:
      - The description of the inventory item
    required: false
    type: str
    version_added: "3.0.0"
  discovered:
    description:
      - Set the discovery flag for the inventory item
    required: false
    default: false
    type: bool
    version_added: "3.0.0"
  label:
    description:
      - The label of the inventory item
    required: false
    type: str
    version_added: "5.12.0"
  parent_inventory_item:
    aliases:
      - parent
    description:
      - The parent item of the inventory item
    required: false
    type: raw
    version_added: "5.12.0"
  software_version:
    description:
      - The software version of the inventory item
    required: false
    type: raw
    version_added: "5.12.0"
  software_image_files:
    description:
      - Override the software image files associated with the software version for this inventory item
    required: false
    type: raw
    version_added: "5.12.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot inventory_item module"
  connection: local
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Create inventory item within Nautobot with only required information
      networktocode.nautobot.inventory_item:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: "10G-SFP+"
        state: present

    - name: Update inventory item
      networktocode.nautobot.inventory_item:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: "10G-SFP+"
        manufacturer: "Cisco"
        part_id: "10G-SFP+"
        serial: "1234"
        asset_tag: "1234"
        description: "New SFP"
        state: present

    - name: Delete inventory item within nautobot
      networktocode.nautobot.inventory_item:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: "10G-SFP+"
        state: absent

    - name: Delete inventory item by id
      networktocode.nautobot.inventory_item:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
inventory_item:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NB_INVENTORY_ITEMS,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            device=dict(required=False, type="raw"),
            name=dict(required=False, type="str"),
            manufacturer=dict(required=False, type="raw"),
            part_id=dict(required=False, type="str"),
            serial=dict(required=False, type="str"),
            asset_tag=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            discovered=dict(required=False, type="bool", default=False),
            label=dict(required=False, type="str"),
            parent_inventory_item=dict(required=False, type="raw", aliases=["parent"]),
            software_version=dict(required=False, type="raw"),
            software_image_files=dict(required=False, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    inventory_item = NautobotDcimModule(module, NB_INVENTORY_ITEMS)
    inventory_item.run()


if __name__ == "__main__":  # pragma: no cover
    main()
