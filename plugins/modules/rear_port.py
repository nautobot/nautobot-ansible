#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rear_port
short_description: Create, update or delete rear ports within Nautobot
description:
  - Creates, updates or removes rear ports from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Tobias Groß (@toerb)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
options:
  device:
    description:
      - The device the rear port is attached to
    required: false
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - The name of the rear port
    required: true
    type: str
    version_added: "3.0.0"
  type:
    description:
      - The type of the rear port
    required: true
    type: str
    version_added: "3.0.0"
  positions:
    description:
      - The number of front ports which may be mapped to each rear port
    required: false
    type: int
    version_added: "3.0.0"
  description:
    description:
      - Description of the rear port
    required: false
    type: str
    version_added: "3.0.0"
  module:
    description:
      - The attached module
    required: false
    type: raw
    version_added: "5.4.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create rear port within Nautobot with only required information
      networktocode.nautobot.rear_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rear Port
        device: Test Device
        type: bnc
        state: present

    - name: Create rear port inside module
      networktocode.nautobot.rear_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rear Port
        module: HooverMaxProModel60
        type: bnc
        state: present

    - name: Update rear port with other fields
      networktocode.nautobot.rear_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rear Port
        device: Test Device
        type: bnc
        positions: 5
        description: rear port description
        state: present

    - name: Delete rear port within nautobot
      networktocode.nautobot.rear_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rear Port
        device: Test Device
        type: bnc
        state: absent
"""

RETURN = r"""
rear_port:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_REAR_PORTS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            device=dict(required=False, type="raw"),
            module=dict(required=False, type="raw"),
            name=dict(required=True, type="str"),
            type=dict(required=True, type="str"),
            positions=dict(required=False, type="int"),
            description=dict(required=False, type="str"),
        )
    )

    required_one_of = [
        ("device", "module"),
    ]
    mutually_exclusive = [
        ("device", "module"),
    ]
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=required_one_of,
        mutually_exclusive=mutually_exclusive,
    )

    rear_port = NautobotDcimModule(module, NB_REAR_PORTS)
    rear_port.run()


if __name__ == "__main__":  # pragma: no cover
    main()
