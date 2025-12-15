#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Jeff Kala (@jeffkala)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: admin_permission
short_description: Create, update or delete object permissions within Nautobot
description:
  - Creates, updates or removes object permissions from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Jeff Kala (@jeffkala)
version_added: "5.3.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
options:
  name:
    description:
      - The name of the permission
      - Required if I(state=present) and the permission does not exist yet
    required: false
    type: str
  description:
    description:
      - The description of the permission
    required: false
    type: str
  enabled:
    description:
      - If the permission is enabled or not.
      - Required if I(state=present) and the permission does not exist yet
    required: false
    type: bool
  object_types:
    description:
      - The permitted object_types for the permission definition.
    required: false
    type: list
    elements: str
  actions:
    description:
      - The actions allowed for the permission definition.
      - Required if I(state=present) and the permission does not exist yet
      - Example actions are: view, add, change, delete, run
    required: false
    type: list
    elements: str
  constraints:
    description:
      - The constraints for the permission definition.
    required: false
    type: raw
  users:
    description:
      - The users assigned for the permission definition.
    required: false
    type: list
    elements: str
  groups:
    description:
      - The groups assigned for the permission definition.
    required: false
    type: list
    elements: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create object permission within Nautobot with only required information
      networktocode.nautobot.admin_permission:
        url: http://nautobot.local
        token: thisIsMyToken
        name: read only
        description: "ro permissions"
        enabled: true
        object_types:
          - "dcim.device"
        actions:
          - view
          - change
        users:
          - nb_user
        groups:
          - read_only_group
        state: present

    - name: Delete permission
      networktocode.nautobot.admin_permission:
        url: http://nautobot.local
        token: thisIsMyToken
        name: read only
        description: "ro permissions"
        enabled: true
        object_types:
          - "dcim.device"
        actions:
          - view
          - change
        users:
          - nb_user
        groups:
          - read_only_group
        state: absent

    - name: Delete permission by id
      networktocode.nautobot.admin_permission:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
admin_permission:
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
    NB_OBJECT_PERMISSION,
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
            name=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            enabled=dict(required=False, type="bool"),
            object_types=dict(required=False, type="list", elements="str"),
            actions=dict(required=False, type="list", elements="str"),
            constraints=dict(required=False, type="raw"),
            users=dict(required=False, type="list", elements="str"),
            groups=dict(required=False, type="list", elements="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    nb_obj_permissions = NautobotUsersModule(module, NB_OBJECT_PERMISSION)
    nb_obj_permissions.run()


if __name__ == "__main__":  # pragma: no cover
    main()
