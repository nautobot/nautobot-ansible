#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ip_address
short_description: Creates or removes ip addresses from Nautobot
description:
  - Creates or removes ip addresses from Nautobot
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
  address:
    required: true
    type: str
  namespace:
    required: false
    type: dict
  type:
    required: false
    type: str
    choices:
      - "dhcp"
      - "host"
      - "slaac"
  dns_name:
    required: false
    type: str
  description:
    required: false
    type: str
  status:
    required: true
    type: str
  role:
    required: false
    type: dict
  parent:
    required: false
    type: dict
  tenant:
    required: false
    type: dict
  nat_inside:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create ip_address within Nautobot with only required information
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: "Test address"
        status: "Active"
        state: present

    - name: Delete ip_address within nautobot
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
ip_address:
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
    NautobotIpamModule,
    NB_IP_ADDRESSES,
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
            address=dict(required=True, type="str"),
            namespace=dict(required=False, type="dict"),
            type=dict(
                required=False,
                type="str",
                choices=[
                    "dhcp",
                    "host",
                    "slaac",
                ],
            ),
            dns_name=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            status=dict(required=True, type="str"),
            role=dict(required=False, type="dict"),
            parent=dict(required=False, type="dict"),
            tenant=dict(required=False, type="dict"),
            nat_inside=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    ip_address = NautobotIpamModule(module, NB_IP_ADDRESSES)
    ip_address.run()


if __name__ == "__main__":  # pragma: no cover
    main()
