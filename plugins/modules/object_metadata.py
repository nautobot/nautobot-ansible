#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: object_metadata
short_description: Creates or removes object metadata from Nautobot
description:
  - Creates or removes object metadata from Nautobot
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
  value:
    required: false
    type: str
  scoped_fields:
    required: false
    type: str
  assigned_object_id:
    required: true
    type: str
  metadata_type:
    required: true
    type: dict
  contact:
    required: false
    type: dict
  team:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create object metadata within Nautobot with only required information
      networktocode.nautobot.object_metadata:
        url: http://nautobot.local
        token: thisIsMyToken
        assigned_object_type: "Test assigned_object_type"
        assigned_object_id: "Test assigned_object_id"
        metadata_type: None
        state: present

    - name: Delete object_metadata within nautobot
      networktocode.nautobot.object_metadata:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
object_metadata:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.extras import (
    NB_OBJECT_METADATA,
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
            value=dict(required=False, type="str"),
            scoped_fields=dict(required=False, type="str"),
            assigned_object_id=dict(required=True, type="str"),
            metadata_type=dict(required=True, type="dict"),
            contact=dict(required=False, type="dict"),
            team=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    object_metadata = NautobotExtrasModule(module, NB_OBJECT_METADATA)
    object_metadata.run()


if __name__ == "__main__":  # pragma: no cover
    main()
