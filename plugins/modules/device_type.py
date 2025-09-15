#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: device_type
short_description: Creates or removes device types from Nautobot
description:
  - Creates or removes device types from Nautobot
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
  front_image:
    required: false
    type: str
  rear_image:
    required: false
    type: str
  model:
    required: true
    type: str
  part_number:
    required: false
    type: str
  u_height:
    required: false
    type: int
  is_full_depth:
    required: false
    type: bool
  subdevice_role:
    required: false
    type: str
    choices:
      - "child"
      - "parent"
  comments:
    required: false
    type: str
  manufacturer:
    required: true
    type: dict
  device_family:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create device type within Nautobot with only required information
      networktocode.nautobot.device_type:
        url: http://nautobot.local
        token: thisIsMyToken
        model: "Test Model"
        manufacturer: None
        state: present

    - name: Delete device_type within nautobot
      networktocode.nautobot.device_type:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
device_type:
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
    NB_DEVICE_TYPES,
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
            front_image=dict(required=False, type="str"),
            rear_image=dict(required=False, type="str"),
            model=dict(required=True, type="str"),
            part_number=dict(required=False, type="str"),
            u_height=dict(required=False, type="int"),
            is_full_depth=dict(required=False, type="bool"),
            subdevice_role=dict(
                required=False,
                type="str",
                choices=[
                    "child",
                    "parent",
                ],
            ),
            comments=dict(required=False, type="str"),
            manufacturer=dict(required=True, type="dict"),
            device_family=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    device_type = NautobotDcimModule(module, NB_DEVICE_TYPES)
    device_type.run()


if __name__ == "__main__":  # pragma: no cover
    main()
