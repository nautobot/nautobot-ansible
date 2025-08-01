#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Jeff Kala (@jeffkala)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: admin_user
short_description: Create, update or delete users within Nautobot
description:
  - Creates, updates or removes users from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Jeff Kala (@jeffkala)
version_added: "5.3.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
options:
  username:
    description:
      - The name of the user
      - Required if I(state=present) and the user does not exist yet
    required: false
    type: str
  is_superuser:
    description:
      - If the user should be set for superuser status
    required: false
    type: bool
  is_staff:
    description:
      - If the user should be set for staff status
    required: false
    type: bool
  is_active:
    description:
      - If the user should be active
    required: false
    type: bool
  first_name:
    description:
      - The first name of the user
    required: false
    type: str
  last_name:
    description:
      - The last name of the user
    required: false
    type: str
  email:
    description:
      - The email of the user
    required: false
    type: str
  groups:
    description:
      - The groups the user is assigned to
    required: false
    type: list
    elements: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create user within Nautobot with only required information
      networktocode.nautobot.admin_user:
        url: http://nautobot.local
        token: thisIsMyToken
        username: nb_user
        email: nb_user@example.com
        first_name: nb
        last_name: user
        state: present

    - name: Delete user within nautobot
      networktocode.nautobot.admin_user:
        url: http://nautobot.local
        token: thisIsMyToken
        username: nb_user
        email: nb_user@example.com
        first_name: nb
        last_name: user
        state: absent

    - name: Delete user by id
      networktocode.nautobot.admin_user:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import ID_ARG_SPEC, NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(
        dict(
            username=dict(required=False, type="str"),
            is_superuser=dict(required=False, type="bool"),
            is_active=dict(required=False, type="bool"),
            is_staff=dict(required=False, type="bool"),
            first_name=dict(required=False, type="str"),
            last_name=dict(required=False, type="str"),
            email=dict(required=False, type="str"),
            groups=dict(required=False, type="list", elements="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    nb_user = NautobotUsersModule(module, NB_USERS)
    nb_user.run()


if __name__ == "__main__":  # pragma: no cover
    main()
