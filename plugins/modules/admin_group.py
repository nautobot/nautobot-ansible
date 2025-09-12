#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Jeff Kala (@jeffkala)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: admin_group
short_description: Create, update or delete admin groups within Nautobot
description:
  - Creates, updates or removes admin groups from Nautobot
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
      - The name of the group
      - Required if I(state=present) and the group does not exist yet
    required: false
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create admin group within Nautobot
      networktocode.nautobot.admin_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: read_only_group
        state: present

    - name: Delete admin group by name
      networktocode.nautobot.admin_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: read_only_group
        state: absent

    - name: Delete admin group by id
      networktocode.nautobot.admin_group:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
admin_group:
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
    NB_ADMIN_GROUP,
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
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    nb_groups = NautobotUsersModule(module, NB_ADMIN_GROUP)
    nb_groups.run()


if __name__ == "__main__":  # pragma: no cover
    main()
