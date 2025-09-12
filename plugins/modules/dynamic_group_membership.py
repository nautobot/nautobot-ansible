#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: dynamic_group_membership
short_description: Creates or removes dynamic group memberships from Nautobot
description:
  - Creates or removes dynamic group memberships from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  id:
    required: false
    type: str
  operator:
    required: true
    type: str
    choices:
      - "union"
      - "intersection"
      - "difference"
  weight:
    required: true
    type: int
  group:
    required: true
    type: dict
  parent_group:
    required: true
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create dynamic_group_membership within Nautobot with only required information
      networktocode.nautobot.dynamic_group_membership:
        url: http://nautobot.local
        token: thisIsMyToken
        operator: union
        weight: None
        group: None
        parent_group: None
        state: present

    - name: Delete dynamic_group_membership within nautobot
      networktocode.nautobot.dynamic_group_membership:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
dynamic_group_membership:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotExtrasModule,
    NB_DYNAMIC_GROUP_MEMBERSHIPS,
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
            operator=dict(
                required=True,
                type="str",
                choices=[
                    "union",
                    "intersection",
                    "difference",
                ],
            ),
            weight=dict(required=True, type="int"),
            group=dict(required=True, type="dict"),
            parent_group=dict(required=True, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    dynamic_group_membership = NautobotExtrasModule(module, NB_DYNAMIC_GROUP_MEMBERSHIPS)
    dynamic_group_membership.run()


if __name__ == "__main__":  # pragma: no cover
    main()
