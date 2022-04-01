#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# Copyright: (c) 2018, David Gomez (@amb1s1) <david.gomez@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: device
short_description: Create, update or delete devices within Nautobot
description:
  - Creates, updates or removes devices from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
  - David Gomez (@amb1s1)
requirements:
  - pynautobot
version_added: "1.0.0"
options:
  url:
    description:
      - URL of the Nautobot instance resolvable by Ansible control host
    required: true
    type: str
  token:
    description:
      - The token created within Nautobot to authorize API access
    required: true
    type: str
  name:
    description:
      - The name of the device
    required: true
    type: str
    version_added: "3.0.0"
  device_type:
    description:
      - Required if I(state=present) and the device does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  device_role:
    description:
      - Required if I(state=present) and the device does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  tenant:
    description:
      - The tenant that the device will be assigned to
    required: false
    type: raw
    version_added: "3.0.0"
  platform:
    description:
      - The platform of the device
    required: false
    type: raw
    version_added: "3.0.0"
  serial:
    description:
      - Serial number of the device
    required: false
    type: str
    version_added: "3.0.0"
  asset_tag:
    description:
      - Asset tag that is associated to the device
    required: false
    type: str
    version_added: "3.0.0"
  site:
    description:
      - Required if I(state=present) and the device does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  rack:
    description:
      - The name of the rack to assign the device to
    required: false
    type: raw
    version_added: "3.0.0"
  position:
    description:
      - The position of the device in the rack defined above
    required: false
    type: int
    version_added: "3.0.0"
  face:
    description:
      - Required if I(rack) is defined
    choices:
      - Front
      - front
      - Rear
      - rear
    required: false
    type: str
    version_added: "3.0.0"
  status:
    description:
      - The status of the device
      - Required if I(state=present) and the device does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  primary_ip4:
    description:
      - Primary IPv4 address assigned to the device
    required: false
    type: raw
    version_added: "3.0.0"
  primary_ip6:
    description:
      - Primary IPv6 address assigned to the device
    required: false
    type: raw
    version_added: "3.0.0"
  cluster:
    description:
      - Cluster that the device will be assigned to
    required: false
    type: raw
    version_added: "3.0.0"
  virtual_chassis:
    description:
      - Virtual chassis the device will be assigned to
    required: false
    type: raw
    version_added: "3.0.0"
  vc_position:
    description:
      - Position in the assigned virtual chassis
    required: false
    type: int
    version_added: "3.0.0"
  vc_priority:
    description:
      - Priority in the assigned virtual chassis
    required: false
    type: int
    version_added: "3.0.0"
  comments:
    description:
      - Comments that may include additional information in regards to the device
    required: false
    type: str
    version_added: "3.0.0"
  tags:
    description:
      - Any tags that the device may need to be associated with
    required: false
    type: list
    elements: raw
    version_added: "3.0.0"
  custom_fields:
    description:
      - must exist in Nautobot
    required: false
    type: dict
    version_added: "3.0.0"
  local_context_data:
    description:
      - Arbitrary JSON data to define the devices configuration variables.
    required: false
    type: dict
    version_added: "3.0.0"
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
    type: str
  query_params:
    description:
      - This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined
      - in plugins/module_utils/utils.py and provides control to users on what may make
      - an object unique in their environment.
    required: false
    type: list
    elements: str
    version_added: "3.0.0"
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
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
        device_role: Core Switch
        site: Main
        status: active
        state: present

    - name: Create device within Nautobot with empty string name to generate UUID
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        name: ""
        device_type: C9410R
        device_role: Core Switch
        site: Main
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
        device_role: Core Switch
        site: Main
        status: active
        local_context_data:
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
    NB_DEVICES,
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
            device_type=dict(required=False, type="raw"),
            device_role=dict(required=False, type="raw"),
            tenant=dict(required=False, type="raw"),
            platform=dict(required=False, type="raw"),
            serial=dict(required=False, type="str"),
            asset_tag=dict(required=False, type="str"),
            site=dict(required=False, type="raw"),
            rack=dict(required=False, type="raw"),
            position=dict(required=False, type="int"),
            face=dict(
                required=False,
                type="str",
                choices=["Front", "front", "Rear", "rear"],
            ),
            status=dict(required=False, type="raw"),
            primary_ip4=dict(required=False, type="raw"),
            primary_ip6=dict(required=False, type="raw"),
            cluster=dict(required=False, type="raw"),
            virtual_chassis=dict(required=False, type="raw"),
            vc_position=dict(required=False, type="int"),
            vc_priority=dict(required=False, type="int"),
            comments=dict(required=False, type="str"),
            tags=dict(required=False, type="list", elements="raw"),
            local_context_data=dict(required=False, type="dict"),
            custom_fields=dict(required=False, type="dict"),
        )
    )

    required_if = [
        ("state", "present", ["name", "status"]),
        ("state", "absent", ["name"]),
    ]

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)
    if module.params["name"] == "":
        module.params["name"] = str(uuid.uuid4())

    device = NautobotDcimModule(module, NB_DEVICES)
    device.run()


if __name__ == "__main__":  # pragma: no cover
    main()
