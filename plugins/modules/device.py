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
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the device
    required: false
    type: str
    version_added: "3.0.0"
  device_type:
    description:
      - Required if I(state=present) and the device does not exist yet
      - Recommended when updating or deleting if not using I(id) or I(name) to aid with identification
    required: false
    type: raw
    version_added: "3.0.0"
  role:
    description:
      - Required if I(state=present) and the device does not exist yet
      - Recommended when updating or deleting if not using I(id) or I(name) to aid with identification
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
  location:
    description:
      - Required if I(state=present) and the device does not exist yet
      - Recommended when updating or deleting if not using I(id) or I(name) to aid with identification
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
  local_config_context_data:
    description:
      - Arbitrary JSON data to define the devices configuration variables.
    required: false
    type: dict
    version_added: "3.0.0"
  device_redundancy_group:
    description:
      - Device redundancy group the device will be assigned to
    required: false
    type: raw
    version_added: "5.1.0"
  controller_managed_device_group:
    description:
      - Device controller_managed_device_group the device will be assigned to
      - Requires Nautobot C(v2.2) or later
    required: false
    type: raw
    version_added: "5.7.0"
  device_redundancy_group_priority:
    description:
      - Priority in the assigned device redundancy group
    required: false
    type: int
    version_added: "5.1.0"
  secrets_group:
    description:
      - The secrets_group of the device
    required: false
    type: raw
    version_added: "5.12.0"
  software_version:
    description:
      - The software version associated with the device
    required: false
    type: raw
    version_added: "5.13.0"
  software_image_files:
    description:
      - Override the software image files associated with the software version for this inventory item
    required: false
    type: raw
    version_added: "5.13.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create device within Nautobot with name
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Device
        device_type: C9410R
        role: Core Switch
        location: My Location
        status: active
        state: present

    - name: Delete device within nautobot with name
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Device
        state: absent

    - name: Rename device via ID
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 15b91de1-448d-4ff7-a00e-0a6816e8bf71
        name: New Name
        state: present

    - name: Delete device via ID
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 15b91de1-448d-4ff7-a00e-0a6816e8bf71
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

    - name: Create device within Nautobot with secrets_group
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        name: TopSecretDevice
        device_type: C9410R
        role: Core Switch
        location: My Location
        secrets_group: "Test Secrets Group"
        status: active
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

import uuid
from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NB_DEVICES,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=False, type="str"),
            device_type=dict(required=False, type="raw"),
            role=dict(required=False, type="raw"),
            tenant=dict(required=False, type="raw"),
            platform=dict(required=False, type="raw"),
            serial=dict(required=False, type="str"),
            asset_tag=dict(required=False, type="str"),
            location=dict(required=False, type="raw"),
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
            local_config_context_data=dict(required=False, type="dict"),
            controller_managed_device_group=dict(required=False, type="raw"),
            device_redundancy_group=dict(required=False, type="raw"),
            device_redundancy_group_priority=dict(required=False, type="int"),
            secrets_group=dict(required=False, type="raw", no_log=False),
            software_version=dict(required=False, type="raw"),
            software_image_files=dict(required=False, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if module.params["name"] == "":
        module.params["name"] = str(uuid.uuid4())

    device = NautobotDcimModule(module, NB_DEVICES)
    device.run()


if __name__ == "__main__":  # pragma: no cover
    main()
