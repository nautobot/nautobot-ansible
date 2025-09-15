#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: controller_managed_device_group
short_description: Creates or removes controller managed device groups from Nautobot
description:
  - Creates or removes controller managed device groups from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  capabilities:
    required: false
    type: list
  name:
    required: true
    type: str
  description:
    required: false
    type: str
  weight:
    required: false
    type: int
  parent:
    required: false
    type: dict
  controller:
    required: true
    type: dict
  tenant:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create controller managed device group within Nautobot with only required information
      networktocode.nautobot.controller_managed_device_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Controller Managed Device Group
        controller: None
        state: present

    - name: Delete controller_managed_device_group within nautobot
      networktocode.nautobot.controller_managed_device_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Controller Managed Device Group
        state: absent
"""

RETURN = r"""
controller_managed_device_group:
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
    NB_CONTROLLER_MANAGED_DEVICE_GROUPS,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            capabilities=dict(required=False, type="list"),
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            weight=dict(required=False, type="int"),
            parent=dict(required=False, type="dict"),
            controller=dict(required=True, type="dict"),
            tenant=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    controller_managed_device_group = NautobotDcimModule(module, NB_CONTROLLER_MANAGED_DEVICE_GROUPS)
    controller_managed_device_group.run()


if __name__ == "__main__":  # pragma: no cover
    main()
