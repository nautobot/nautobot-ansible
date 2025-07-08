#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: role
short_description: Create, update or delete roles within Nautobot
description:
  - Creates, updates or removes roles from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
version_added: "5.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the role
    required: true
    type: str
    version_added: "5.0.0"
  description:
    description:
      - The description of the role
    required: false
    type: str
    version_added: "5.0.0"
  color:
    description:
      - Hexidecimal code for a color, ex. FFFFFF
    required: false
    type: str
    version_added: "5.0.0"
  content_types:
    description:
      - Model names which the role can be related to.
    type: list
    elements: str
    version_added: "5.0.0"
  weight:
    description:
      - Weight assigned to the role.
    type: int
    version_added: "5.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create role within Nautobot with only required information
      networktocode.nautobot.role:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test role
        color: FFFFFF
        content_types:
          - "dcim.device"
        state: present

    - name: Delete role within nautobot
      networktocode.nautobot.role:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test role
        state: absent
"""

RETURN = r"""
role:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""
from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NB_ROLES,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            color=dict(required=False, type="str"),
            content_types=dict(required=False, type="list", elements="str"),
            weight=dict(required=False, type="int"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    role = NautobotDcimModule(module, NB_ROLES)
    role.run()


if __name__ == "__main__":  # pragma: no cover
    main()
