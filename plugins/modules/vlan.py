#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: vlan
short_description: Creates or removes vlans from Nautobot
description:
  - Creates or removes vlans from Nautobot
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
  location:
    required: false
    type: dict
  vid:
    required: true
    type: int
  name:
    required: true
    type: str
  description:
    required: false
    type: str
  vlan_group:
    required: false
    type: dict
  status:
    required: true
    type: str
  role:
    required: false
    type: dict
  tenant:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create vlan within Nautobot with only required information
      networktocode.nautobot.vlan:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Vlan
        vid: None
        status: "Active"
        state: present

    - name: Delete vlan within nautobot
      networktocode.nautobot.vlan:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Vlan
        state: absent
"""

RETURN = r"""
vlan:
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
    NB_VLANS,
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
            location=dict(required=False, type="dict"),
            vid=dict(required=True, type="int"),
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            vlan_group=dict(required=False, type="dict"),
            status=dict(required=True, type="str"),
            role=dict(required=False, type="dict"),
            tenant=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    vlan = NautobotIpamModule(module, NB_VLANS)
    vlan.run()


if __name__ == "__main__":  # pragma: no cover
    main()
