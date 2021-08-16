#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

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
  device:
    description:
      - The device the device bay will be associated to. The device type must be "parent".
    required: false
    type: raw
  name:
    description:
      - The name of the device bay
    required: true
    type: str
  description:
    description:
      - The description of the device bay. This is supported on v2.6+ of Nautobot
    required: false
    type: str
  installed_device:
    description:
      - The ddevice that will be installed into the bay. The device type must be "child".
    required: false
    type: raw
  tags:
    description:
      - Any tags that the device bay may need to be associated with
    required: false
    type: list
    elements: raw
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

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_DEVICE_BAYS,
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
            device=dict(required=False, type="raw"),
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            installed_device=dict(required=False, type="raw"),
            tags=dict(required=False, type="list", elements="raw"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    device_bay = NautobotDcimModule(module, NB_DEVICE_BAYS)
    device_bay.run()


if __name__ == "__main__":  # pragma: no cover
    main()
