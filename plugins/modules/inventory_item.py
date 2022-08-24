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
requirements:
  - pynautobot
version_added: "1.0.0"
options:
  api_version:
    description:
      - API Version Nautobot REST API
    required: false
    type: str
    version_added: "4.1.0"
  url:
    description:
      - URL of the Nautobot instance resolvable by Ansible control host
    required: true
    type: str
  token:
    description:
      - The token created within Nautobot to authorize API access
    required: true
    type: str
  device:
    description:
      - Name of the device the inventory item belongs to
    required: true
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - Name of the inventory item to be created
    required: true
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
  tags:
    description:
      - Any tags that the device may need to be associated with
    required: false
    type: list
    elements: raw
    version_added: "3.0.0"
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
    type: str
  query_params:
    description:
      - This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined
      - in plugins/module_utils/utils.py and provides control to users on what may make
      - an object unique in their environment.
    required: false
    type: list
    elements: str
    version_added: "3.0.0"
  validate_certs:
    description:
      - |
        If C(no), SSL certificates will not be validated.
        This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot inventory_item module"
  connection: local
  hosts: localhost
  gather_facts: False
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

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
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
    argument_spec.update(
        dict(
            device=dict(required=True, type="raw"),
            name=dict(required=True, type="str"),
            manufacturer=dict(required=False, type="raw"),
            part_id=dict(required=False, type="str"),
            serial=dict(required=False, type="str"),
            asset_tag=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            discovered=dict(required=False, type="bool", default=False),
            tags=dict(required=False, type="list", elements="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    inventory_item = NautobotDcimModule(module, NB_INVENTORY_ITEMS)
    inventory_item.run()


if __name__ == "__main__":  # pragma: no cover
    main()
