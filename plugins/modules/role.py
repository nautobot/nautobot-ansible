#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: role
short_description: Creates or removes roles from Nautobot
description:
  - Creates or removes roles from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  content_types:
    required: true
    type: list
  name:
    required: true
    type: str
  color:
    required: false
    type: str
  description:
    required: false
    type: str
  weight:
    required: false
    type: int
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create role within Nautobot with only required information
      networktocode.nautobot.role:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Role
        content_types: None
        state: present

    - name: Delete role within nautobot
      networktocode.nautobot.role:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Role
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

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import CUSTOM_FIELDS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotExtrasModule,
    NB_ROLES,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            content_types=dict(required=True, type="list"),
            name=dict(required=True, type="str"),
            color=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            weight=dict(required=False, type="int"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    role = NautobotExtrasModule(module, NB_ROLES)
    role.run()


if __name__ == "__main__":  # pragma: no cover
    main()
