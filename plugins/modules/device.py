#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: device
short_description: Creates or removes devices from Nautobot
description:
  - Creates or removes devices from Nautobot
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
  local_config_context_data:
    required: false
    type: str
  local_config_context_data_owner_object_id:
    required: false
    type: str
  name:
    required: false
    type: str
  serial:
    required: false
    type: str
  asset_tag:
    required: false
    type: str
  position:
    required: false
    type: int
  face:
    required: false
    type: str
    choices:
      - "front"
      - "rear"
  device_redundancy_group_priority:
    required: false
    type: int
  vc_position:
    required: false
    type: int
  vc_priority:
    required: false
    type: int
  comments:
    required: false
    type: str
  local_config_context_schema:
    required: false
    type: dict
  local_config_context_data_owner_content_type:
    required: false
    type: dict
  device_type:
    required: true
    type: dict
  status:
    required: true
    type: str
  role:
    required: true
    type: dict
  tenant:
    required: false
    type: dict
  platform:
    required: false
    type: dict
  location:
    required: true
    type: dict
  rack:
    required: false
    type: dict
  primary_ip4:
    required: false
    type: dict
  primary_ip6:
    required: false
    type: dict
  cluster:
    required: false
    type: dict
  virtual_chassis:
    required: false
    type: dict
  device_redundancy_group:
    required: false
    type: dict
  software_version:
    required: false
    type: dict
  secrets_group:
    required: false
    type: dict
  controller_managed_device_group:
    required: false
    type: dict
  software_image_files:
    required: false
    type: list
  parent_bay:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create device within Nautobot with only required information
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        device_type: None
        status: "Active"
        role: None
        location: None
        state: present

    - name: Delete device within nautobot
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import CUSTOM_FIELDS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import TAGS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_DEVICES,
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
            local_config_context_data=dict(required=False, type="str"),
            local_config_context_data_owner_object_id=dict(required=False, type="str"),
            name=dict(required=False, type="str"),
            serial=dict(required=False, type="str"),
            asset_tag=dict(required=False, type="str"),
            position=dict(required=False, type="int"),
            face=dict(
                required=False,
                type="str",
                choices=[
                    "front",
                    "rear",
                ],
            ),
            device_redundancy_group_priority=dict(required=False, type="int"),
            vc_position=dict(required=False, type="int"),
            vc_priority=dict(required=False, type="int"),
            comments=dict(required=False, type="str"),
            local_config_context_schema=dict(required=False, type="dict"),
            local_config_context_data_owner_content_type=dict(required=False, type="dict"),
            device_type=dict(required=True, type="dict"),
            status=dict(required=True, type="str"),
            role=dict(required=True, type="dict"),
            tenant=dict(required=False, type="dict"),
            platform=dict(required=False, type="dict"),
            location=dict(required=True, type="dict"),
            rack=dict(required=False, type="dict"),
            primary_ip4=dict(required=False, type="dict"),
            primary_ip6=dict(required=False, type="dict"),
            cluster=dict(required=False, type="dict"),
            virtual_chassis=dict(required=False, type="dict"),
            device_redundancy_group=dict(required=False, type="dict"),
            software_version=dict(required=False, type="dict"),
            secrets_group=dict(required=False, type="dict"),
            controller_managed_device_group=dict(required=False, type="dict"),
            software_image_files=dict(required=False, type="list"),
            parent_bay=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    device = NautobotDcimModule(module, NB_DEVICES)
    device.run()


if __name__ == "__main__":  # pragma: no cover
    main()
