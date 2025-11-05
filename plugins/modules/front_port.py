#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: front_port
short_description: Create, update or delete front ports within Nautobot
description:
  - Creates, updates or removes front ports from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Tobias Groß (@toerb)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  device:
    description:
      - The device the front port is attached to
      - Requires one of I(device) or I(module) when I(state=present) and the front port does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - The name of the front port
      - Required if I(state=present) and the front port does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  type:
    description:
      - The type of the front port
      - Required if I(state=present) and the front port does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  rear_port:
    description:
      - The rear_port the front port is attached to
      - Required if I(state=present) and the front port does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  rear_port_position:
    description:
      - The position of the rear port this front port is connected to
    required: false
    type: int
    version_added: "3.0.0"
  description:
    description:
      - Description of the front port
    required: false
    type: str
    version_added: "3.0.0"
  module:
    description:
      - The attached module
      - Requires one of I(device) or I(module) when I(state=present) and the front port does not exist yet
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
    - name: Create front port within Nautobot with only required information
      networktocode.nautobot.front_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Front Port
        device: Test Device
        type: bnc
        rear_port: Test Rear Port
        state: present

    - name: Create front port inside module
      networktocode.nautobot.front_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Front Port
        module: HooverMaxProModel60
        type: bnc
        rear_port: Test Rear Port
        state: present

    - name: Update front port with other fields
      networktocode.nautobot.front_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Front Port
        device: Test Device
        type: bnc
        rear_port: Test Rear Port
        rear_port_position: 5
        description: front port description
        state: present

    - name: Delete front port within nautobot
      networktocode.nautobot.front_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Front Port
        device: Test Device
        type: bnc
        rear_port: Test Rear Port
        state: absent

    - name: Delete front port by id
      networktocode.nautobot.front_port:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
front_port:
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
    NB_FRONT_PORTS,
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
            device=dict(required=False, type="raw"),
            module=dict(required=False, type="raw"),
            name=dict(required=False, type="str"),
            type=dict(required=False, type="str"),
            rear_port=dict(required=False, type="raw"),
            rear_port_position=dict(required=False, type="int"),
            description=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    front_port = NautobotDcimModule(module, NB_FRONT_PORTS)
    front_port.run()


if __name__ == "__main__":  # pragma: no cover
    main()
