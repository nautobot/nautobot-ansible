#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: static_group_association
short_description: Creates or removes static group associations from Nautobot
description:
  - Creates or removes static group associations from Nautobot
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
  associated_object_type:
    required: true
    type: str
  associated_object_id:
    required: true
    type: str
  dynamic_group:
    required: true
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create static_group_association within Nautobot with only required information
      networktocode.nautobot.static_group_association:
        url: http://nautobot.local
        token: thisIsMyToken
        associated_object_type: "Test associated_object_type"
        associated_object_id: "Test associated_object_id"
        dynamic_group: None
        state: present

    - name: Delete static_group_association within nautobot
      networktocode.nautobot.static_group_association:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
static_group_association:
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
    NB_STATIC_GROUP_ASSOCIATIONS,
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
            associated_object_type=dict(required=True, type="str"),
            associated_object_id=dict(required=True, type="str"),
            dynamic_group=dict(required=True, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    static_group_association = NautobotExtrasModule(module, NB_STATIC_GROUP_ASSOCIATIONS)
    static_group_association.run()


if __name__ == "__main__":  # pragma: no cover
    main()
