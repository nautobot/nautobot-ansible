#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: note
short_description: Creates or removes notes from Nautobot
description:
  - Creates or removes notes from Nautobot
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
  assigned_object_type:
    required: true
    type: str
  assigned_object_id:
    required: true
    type: str
  note:
    required: true
    type: str
  user:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create note within Nautobot with only required information
      networktocode.nautobot.note:
        url: http://nautobot.local
        token: thisIsMyToken
        assigned_object_type: "Test assigned_object_type"
        assigned_object_id: "Test assigned_object_id"
        note: "Test note"
        state: present

    - name: Delete note within nautobot
      networktocode.nautobot.note:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
note:
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
    NB_NOTES,
    NautobotExtrasModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            assigned_object_type=dict(required=True, type="str"),
            assigned_object_id=dict(required=True, type="str"),
            note=dict(required=True, type="str"),
            user=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    note = NautobotExtrasModule(module, NB_NOTES)
    note.run()


if __name__ == "__main__":  # pragma: no cover
    main()
