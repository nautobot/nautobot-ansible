#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: device_bay
short_description: Create, update or delete device bays within Nautobot
description:
  - Creates, updates or removes device bays from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  device:
    description:
      - The device the device bay will be associated to. The device type must be "parent".
    required: false
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - The name of the device bay
      - Required if I(state=present) and the device bay does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  description:
    description:
      - The description of the device bay.
    required: false
    type: str
    version_added: "3.0.0"
  installed_device:
    description:
      - The device that will be installed into the bay. The device type must be "child".
    required: false
    type: raw
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create device bay within Nautobot with only required information
      networktocode.nautobot.device_bay:
        url: http://nautobot.local
        token: thisIsMyToken
        device: Test Nexus One
        name: "Device Bay One"
        state: present

    - name: Add device into device bay
      networktocode.nautobot.device_bay:
        url: http://nautobot.local
        token: thisIsMyToken
        device: Test Nexus One
        name: "Device Bay One"
        description: "First child"
        installed_device: Test Nexus Child One
        state: absent

    - name: Delete device bay within nautobot
      networktocode.nautobot.device_bay:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Device Bay One
        state: absent

    - name: Delete device bay by id
      networktocode.nautobot.device_bay:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
device_bay:
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
    NB_DEVICE_BAYS,
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
            name=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            installed_device=dict(required=False, type="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    device_bay = NautobotDcimModule(module, NB_DEVICE_BAYS)
    device_bay.run()


if __name__ == "__main__":  # pragma: no cover
    main()
