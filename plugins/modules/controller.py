#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: controller
short_description: Creates or removes controllers from Nautobot
description:
  - Creates or removes controllers from Nautobot
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
  status:
    required: true
    type: str
  location:
    required: true
    type: dict
  platform:
    required: false
    type: dict
  role:
    required: false
    type: dict
  tenant:
    required: false
    type: dict
  external_integration:
    required: false
    type: dict
  controller_device:
    required: false
    type: dict
  controller_device_redundancy_group:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create controller within Nautobot with only required information
      networktocode.nautobot.controller:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Controller
        status: "Active"
        location: None
        state: present

    - name: Delete controller within nautobot
      networktocode.nautobot.controller:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Controller
        state: absent
"""

RETURN = r"""
controller:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import TAGS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_CONTROLLERS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


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
            status=dict(required=True, type="str"),
            location=dict(required=True, type="dict"),
            platform=dict(required=False, type="dict"),
            role=dict(required=False, type="dict"),
            tenant=dict(required=False, type="dict"),
            external_integration=dict(required=False, type="dict"),
            controller_device=dict(required=False, type="dict"),
            controller_device_redundancy_group=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    controller = NautobotDcimModule(module, NB_CONTROLLERS)
    controller.run()


if __name__ == "__main__":  # pragma: no cover
    main()
