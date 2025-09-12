#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: interface_redundancy_group
short_description: Creates or removes interface redundancy groups from Nautobot
description:
  - Creates or removes interface redundancy groups from Nautobot
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
  description:
    required: false
    type: str
  protocol:
    required: false
    type: str
    choices:
      - "hsrp"
      - "vrrp"
      - "glbp"
      - "carp"
  protocol_group_id:
    required: false
    type: str
  status:
    required: true
    type: str
  secrets_group:
    required: false
    type: dict
  virtual_ip:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create interface_redundancy_group within Nautobot with only required information
      networktocode.nautobot.interface_redundancy_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Interface_Redundancy_Group
        status: "Active"
        state: present

    - name: Delete interface_redundancy_group within nautobot
      networktocode.nautobot.interface_redundancy_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Interface_Redundancy_Group
        state: absent
"""

RETURN = r"""
interface_redundancy_group:
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
    NB_INTERFACE_REDUNDANCY_GROUPS,
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
            description=dict(required=False, type="str"),
            protocol=dict(
                required=False,
                type="str",
                choices=[
                    "hsrp",
                    "vrrp",
                    "glbp",
                    "carp",
                ],
            ),
            protocol_group_id=dict(required=False, type="str"),
            status=dict(required=True, type="str"),
            secrets_group=dict(required=False, type="dict"),
            virtual_ip=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    interface_redundancy_group = NautobotDcimModule(module, NB_INTERFACE_REDUNDANCY_GROUPS)
    interface_redundancy_group.run()


if __name__ == "__main__":  # pragma: no cover
    main()
