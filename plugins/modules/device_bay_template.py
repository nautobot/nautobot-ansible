#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: device_bay_template
short_description: Creates or removes device bay templates from Nautobot
description:
  - Creates or removes device bay templates from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  name:
    required: true
    type: str
  label:
    required: false
    type: str
  description:
    required: false
    type: str
  device_type:
    required: true
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create device_bay_template within Nautobot with only required information
      networktocode.nautobot.device_bay_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Device_Bay_Template
        device_type: None
        state: present

    - name: Delete device_bay_template within nautobot
      networktocode.nautobot.device_bay_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Device_Bay_Template
        state: absent
"""

RETURN = r"""
device_bay_template:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_DEVICE_BAY_TEMPLATES,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            label=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            device_type=dict(required=True, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    device_bay_template = NautobotDcimModule(module, NB_DEVICE_BAY_TEMPLATES)
    device_bay_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
