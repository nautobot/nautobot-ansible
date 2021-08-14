#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
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
module: device_type
short_description: Create, update or delete device types within Nautobot
description:
  - Creates, updates or removes device types from Nautobot
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
  manufacturer:
    description:
      - The manufacturer of the device type
    required: false
    type: raw
  model:
    description:
      - The model of the device type
    required: true
    type: raw
  slug:
    description:
      - The slug of the device type. Must follow slug formatting (URL friendly)
      - If not specified, it will slugify the model
      - ex. test-device-type
    required: false
    type: str
  part_number:
    description:
      - The part number of the device type
    required: false
    type: str
  u_height:
    description:
      - The height of the device type in rack units
    required: false
    type: int
  is_full_depth:
    description:
      - Whether or not the device consumes both front and rear rack faces
    required: false
    type: bool
  subdevice_role:
    description:
      - Whether the device type is parent, child, or neither
    choices:
      - Parent
      - parent
      - Child
      - child
    required: false
    type: str
  comments:
    description:
      - Comments that may include additional information in regards to the device_type
    required: false
    type: str
  tags:
    description:
      - Any tags that the device type may need to be associated with
    required: false
    type: list
    elements: raw
  custom_fields:
    description:
      - must exist in Nautobot
    required: false
    type: dict
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
    - name: Create device type within Nautobot with only required information
      networktocode.nautobot.device_type:
        url: http://nautobot.local
        token: thisIsMyToken
        slug: test-device-type
        model: ws-test-3750
        manufacturer: Test Manufacturer
        state: present

    - name: Create device type within Nautobot with only required information
      networktocode.nautobot.device_type:
        url: http://nautobot.local
        token: thisIsMyToken
        slug: test-device-type
        model: ws-test-3750
        manufacturer: Test Manufacturer
        part_number: ws-3750g-v2
        u_height: 1
        is_full_depth: False
        subdevice_role: parent
        state: present

    - name: Delete device type within nautobot
      networktocode.nautobot.device_type:
        url: http://nautobot.local
        token: thisIsMyToken
        slug: test-device-type
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

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_DEVICE_TYPES,
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
            manufacturer=dict(required=False, type="raw"),
            model=dict(required=True, type="raw"),
            slug=dict(required=False, type="str"),
            part_number=dict(required=False, type="str"),
            u_height=dict(required=False, type="int"),
            is_full_depth=dict(required=False, type="bool"),
            subdevice_role=dict(
                required=False,
                choices=["Parent", "parent", "Child", "child"],
                type="str",
            ),
            comments=dict(required=False, type="str"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    device_type = NautobotDcimModule(module, NB_DEVICE_TYPES)
    device_type.run()


if __name__ == "__main__":  # pragma: no cover
    main()
