#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: device_interface_template
short_description: Creates or removes interfaces on devices from Nautobot
description:
  - Creates or removes interfaces from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Tobias Groß (@toerb)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
options:
  device_type:
    description:
      - Name of the device the interface template will be associated with (case-sensitive)
      - Requires one of I(device_type) or I(module_type) when I(state=present) and the interface template does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - Name of the interface template to be created
      - Required if I(state=present) and the interface template does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  type:
    description:
      - |
        Form factor of the interface:
        ex. 1000Base-T (1GE), Virtual, 10GBASE-T (10GE)
        This has to be specified exactly as what is found within UI
      - Required if I(state=present) and the interface template does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  mgmt_only:
    description:
      - This interface template is used only for out-of-band management
    required: false
    type: bool
    version_added: "3.0.0"
  label:
    description:
      - Label of the interface template to be created
    required: false
    type: str
    version_added: "5.2.0"
  description:
    description:
      - Description of the interface
    required: false
    type: str
    version_added: "5.2.0"
  module_type:
    description:
      - The module type the interface template is attached to
      - Requires one of I(device_type) or I(module_type) when I(state=present) and the interface template does not exist yet
    required: false
    type: raw
    version_added: "5.4.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot interface template module"
  connection: local
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Create interface template within Nautobot with only required information
      networktocode.nautobot.device_interface_template:
        url: http://nautobot.local
        token: thisIsMyToken
        device_type: Arista Test
        name: 10GBASE-T (10GE)
        type: 10gbase-t
        state: present
    - name: Delete interface template within nautobot
      networktocode.nautobot.device_interface_template:
        url: http://nautobot.local
        token: thisIsMyToken
        device_type: Arista Test
        name: 10GBASE-T (10GE)
        type: 10gbase-t
        state: absent

    - name: Delete interface template by id
      networktocode.nautobot.device_interface_template:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
interface_template:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NB_INTERFACE_TEMPLATES,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import ID_ARG_SPEC, NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(
        dict(
            device_type=dict(required=False, type="raw"),
            name=dict(required=False, type="str"),
            type=dict(required=False, type="str"),
            mgmt_only=dict(required=False, type="bool"),
            label=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            module_type=dict(required=False, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    device_interface_template = NautobotDcimModule(module, NB_INTERFACE_TEMPLATES)
    device_interface_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
