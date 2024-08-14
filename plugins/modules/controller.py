#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: controller
short_description: Create, update or delete controllers within Nautobot
description:
  - Creates, updates or removes controllers from Nautobot.
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Josh VanDeraa (@jvanderaa)
version_added: "5.3.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the controller
    required: true
    type: str
  description:
    description:
      - Description of the controller
    required: false
    type: str
  controller_device:
    description:
      - Device that runs the controller software
    required: false
    type: str
  external_integration:
    description:
      - External connection for the controller, such as Meraki Cloud URL
    required: false
    type: str
  role:
    description:
      - Required if I(state=present) and the controller does not exist yet
    required: false
    type: raw
  tenant:
    description:
      - The tenant that the controller will be assigned to
    required: false
    type: raw
  platform:
    description:
      - The platform of the controller
    required: false
    type: raw
  location:
    description:
      - Required if I(state=present) and the controller does not exist yet
    required: false
    type: raw
  status:
    description:
      - The status of the controller
      - Required if I(state=present) and the controller does not exist yet
    required: false
    type: raw
  controller_device_redundancy_group:
    description:
      - Related device redundancy group the controller will be assigned to
    required: false
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create controller within Nautobot with only required information
      networktocode.nautobot.controller:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "test_controller_2"
        location: My Location
        status: "Active"
        state: present

    - name: "CREATE THE SECOND CONTROLLER"
      networktocode.nautobot.controller:
        name: "test_controller_3"
        url: http://nautobot.local
        token: thisIsMyToken
        status: "Active"
        description: "Description of the controller"
        location: "Cisco"
        external_integration: "Cisco Catalyst SD-WAN"
        role: "Administrative"
        platform: "Cisco IOS"
        tenant: "Nautobot Baseball Stadiums"
        controller_device_redundancy_group: "controller_test"

    - name: Delete controller within nautobot
      networktocode.nautobot.controller:
        url: http://nautobot.local
        token: thisIsMyToken
        name: test_controller_3
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
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            controller_device=dict(required=False, type="str"),
            external_integration=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            location=dict(required=False, type="raw"),
            role=dict(required=False, type="raw"),
            tenant=dict(required=False, type="raw"),
            platform=dict(required=False, type="raw"),
            status=dict(required=False, type="raw"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
            controller_device_redundancy_group=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    controller = NautobotDcimModule(module, NB_CONTROLLERS)
    controller.run()


if __name__ == "__main__":  # pragma: no cover
    main()
