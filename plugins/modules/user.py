#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: user
short_description: Creates or removes users from Nautobot
description:
  - Creates or removes users from Nautobot
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
  password:
    required: false
    type: str
  last_login:
    required: false
    type: str
  is_superuser:
    required: false
    type: bool
  username:
    required: true
    type: str
  first_name:
    required: false
    type: str
  last_name:
    required: false
    type: str
  email:
    required: false
    type: str
  is_staff:
    required: false
    type: bool
  is_active:
    required: false
    type: bool
  date_joined:
    required: false
    type: str
  config_data:
    required: false
    type: str
  groups:
    required: false
    type: list
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create user within Nautobot with only required information
      networktocode.nautobot.user:
        url: http://nautobot.local
        token: thisIsMyToken
        username: "Test Username"
        state: present

    - name: Delete user within nautobot
      networktocode.nautobot.user:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
user:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.users import (
    NB_USERS,
    NautobotUsersModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            password=dict(required=False, type="str"),
            last_login=dict(required=False, type="str"),
            is_superuser=dict(required=False, type="bool"),
            username=dict(required=True, type="str"),
            first_name=dict(required=False, type="str"),
            last_name=dict(required=False, type="str"),
            email=dict(required=False, type="str"),
            is_staff=dict(required=False, type="bool"),
            is_active=dict(required=False, type="bool"),
            date_joined=dict(required=False, type="str"),
            config_data=dict(required=False, type="str"),
            groups=dict(required=False, type="list"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    user = NautobotUsersModule(module, NB_USERS)
    user.run()


if __name__ == "__main__":  # pragma: no cover
    main()
