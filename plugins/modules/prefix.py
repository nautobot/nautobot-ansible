#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: prefix
short_description: Creates or removes prefixes from Nautobot
description:
  - Creates or removes prefixes from Nautobot
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
  prefix:
    required: true
    type: str
  location:
    required: false
    type: dict
  type:
    required: false
    type: str
    choices:
      - "container"
      - "network"
      - "pool"
  date_allocated:
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
  namespace:
    required: false
    type: dict
  tenant:
    required: false
    type: dict
  vlan:
    required: false
    type: dict
  rir:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create prefix within Nautobot with only required information
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        prefix: "Test prefix"
        status: "Active"
        state: present

    - name: Delete prefix within nautobot
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
prefix:
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
    NB_PREFIXES,
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
            prefix=dict(required=True, type="str"),
            location=dict(required=False, type="dict"),
            type=dict(
                required=False,
                type="str",
                choices=[
                    "container",
                    "network",
                    "pool",
                ],
            ),
            date_allocated=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            status=dict(required=True, type="str"),
            role=dict(required=False, type="dict"),
            parent=dict(required=False, type="dict"),
            namespace=dict(required=False, type="dict"),
            tenant=dict(required=False, type="dict"),
            vlan=dict(required=False, type="dict"),
            rir=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    prefix = NautobotIpamModule(module, NB_PREFIXES)
    prefix.run()


if __name__ == "__main__":  # pragma: no cover
    main()
