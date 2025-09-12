#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: device_types_to_software_image_file
short_description: Creates or removes device types to software image files from Nautobot
description:
  - Creates or removes device types to software image files from Nautobot
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
  device_type:
    required: true
    type: dict
  software_image_file:
    required: true
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create device_types_to_software_image_file within Nautobot with only required information
      networktocode.nautobot.device_types_to_software_image_file:
        url: http://nautobot.local
        token: thisIsMyToken
        device_type: None
        software_image_file: None
        state: present

    - name: Delete device_types_to_software_image_file within nautobot
      networktocode.nautobot.device_types_to_software_image_file:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
device_types_to_software_image_file:
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
    NB_DEVICE_TYPES_TO_SOFTWARE_IMAGE_FILES,
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
            device_type=dict(required=True, type="dict"),
            software_image_file=dict(required=True, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    device_types_to_software_image_file = NautobotDcimModule(module, NB_DEVICE_TYPES_TO_SOFTWARE_IMAGE_FILES)
    device_types_to_software_image_file.run()


if __name__ == "__main__":  # pragma: no cover
    main()
