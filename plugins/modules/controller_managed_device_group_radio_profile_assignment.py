#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: controller_managed_device_group_radio_profile_assignment
short_description: Creates or removes controller managed device group radio profile assignments from Nautobot
description:
  - Creates or removes controller managed device group radio profile assignments from Nautobot
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
  controller_managed_device_group:
    required: true
    type: dict
  radio_profile:
    required: true
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create controller_managed_device_group_radio_profile_assignment within Nautobot with only required information
      networktocode.nautobot.controller_managed_device_group_radio_profile_assignment:
        url: http://nautobot.local
        token: thisIsMyToken
        controller_managed_device_group: None
        radio_profile: None
        state: present

    - name: Delete controller_managed_device_group_radio_profile_assignment within nautobot
      networktocode.nautobot.controller_managed_device_group_radio_profile_assignment:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
controller_managed_device_group_radio_profile_assignment:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotWirelessModule,
    NB_CONTROLLER_MANAGED_DEVICE_GROUP_RADIO_PROFILE_ASSIGNMENTS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            controller_managed_device_group=dict(required=True, type="dict"),
            radio_profile=dict(required=True, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    controller_managed_device_group_radio_profile_assignment = NautobotWirelessModule(module, NB_CONTROLLER_MANAGED_DEVICE_GROUP_RADIO_PROFILE_ASSIGNMENTS)
    controller_managed_device_group_radio_profile_assignment.run()


if __name__ == "__main__":  # pragma: no cover
    main()
