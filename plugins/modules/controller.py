#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2023, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# TODO: Check for any words of Device

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: controller
short_description: Create, update or delete controllers within Nautobot
description:
  - Creates, updates or removes controllers from Nautobot, related page: https://docs.nautobot.com/projects/core/en/stable/user-guide/core-data-model/dcim/controller/
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
    version_added: "5.3.0"
  controller_device:
    description:
      - Device that runs the controller software
    required: false
    type: string
    version_added: "5.3.0"
  external_integration:
    description:
      - External connection for the controller, such as Meraki Cloud URL
    required: false
    type: string
    version_added: "5.3.0"
  role:
    description:
      - Required if I(state=present) and the device does not exist yet
    required: false
    type: raw
    version_added: "5.3.0"
  tenant:
    description:
      - The tenant that the device will be assigned to
    required: false
    type: raw
    version_added: "5.3.0"
  platform:
    description:
      - The platform of the device
    required: false
    type: raw
    version_added: "5.3.0"
  location:
    description:
      - Required if I(state=present) and the device does not exist yet
    required: false
    type: raw
    version_added: "5.3.0"
  status:
    description:
      - The status of the device
      - Required if I(state=present) and the device does not exist yet
    required: false
    type: raw
    version_added: "5.3.0"
  local_config_context_data:
    description:
      - Arbitrary JSON data to define the devices configuration variables.
    required: false
    type: dict
    version_added: "5.3.0"
  device_redundancy_group:
    description:
      - Device redundancy group the device will be assigned to
    required: false
    type: raw
    version_added: "5.1.0"
  controller_device_redundancy_group:
    description:
      - Related device redundancy group the device will be assigned to
    required: false
    type: string
    version_added: "5.3.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create device within Nautobot with only required information
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Device
        device_type: C9410R
        role: Core Switch
        location: My Location
        status: active
        state: present

    - name: Create device within Nautobot with empty string name to generate UUID
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        name: ""
        device_type: C9410R
        role: Core Switch
        location:
          name: My Location
          parent: Parent Location
        status: active
        state: present

    - name: Delete device within nautobot
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Device
        state: absent

    - name: Create device with tags
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Another Test Device
        device_type: C9410R
        role: Core Switch
        location:
          name: My Location
          parent: Parent Location
        status: active
        local_config_context_data:
          bgp: "65000"
        tags:
          - Schnozzberry
        state: present

    - name: Update the rack and position of an existing device
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Device
        rack: Test Rack
        position: 10
        face: Front
        state: present
"""

RETURN = r"""
device:
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
import uuid


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
            role=dict(required=False, type="raw"),
            tenant=dict(required=False, type="raw"),
            platform=dict(required=False, type="raw"),
            location=dict(required=False, type="raw"),
            status=dict(required=False, type="raw"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
            controller_device_redundancy_group=dict(required=False, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if module.params["name"] == "":
        module.params["name"] = str(uuid.uuid4())

    controller = NautobotDcimModule(module, NB_CONTROLLERS)
    controller.run()


if __name__ == "__main__":  # pragma: no cover
    main()
