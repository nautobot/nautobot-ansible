#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2023, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: location_type
short_description: Creates or removes location types from Nautobot
description:
  - Creates or removes location types from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Joe Wesch (@joewesch)
requirements:
  - pynautobot
version_added: "4.3.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - Name of the location type to be created
    required: true
    type: str
  description:
    description:
      - Location Type description
    required: false
    type: str
  parent_location_type:
    aliases:
      - parent
    description:
      - The parent location type this location type should be tied to
    required: false
    type: raw
  nestable:
    description:
      - Allow Locations of this type to be parents/children of other Locations of this same type
      - Requires C(nautobot >= 1.5)
    type: bool
  content_types:
    description:
      - Location Type content type(s). These match app.endpoint and the endpoint is singular.
      - e.g. dcim.device, ipam.ipaddress (more can be found in the examples)
    required: false
    type: list
    elements: str
"""

EXAMPLES = r"""
- name: "Test Nautobot location type module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create location type
      networktocode.nautobot.location_type:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Location Type
        state: present

    - name: Delete location type
      networktocode.nautobot.location_type:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Location Type
        state: absent

    - name: Create location type with all parameters
      networktocode.nautobot.location_type:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Nested Location Type
        description: My Nested Location Type Description
        parent:
          name: My Location Type
        nestable: false
        content_types:
          - "dcim.device"
        state: present
"""

RETURN = r"""
location_type:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_LOCATION_TYPES,
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
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            parent_location_type=dict(required=False, type="raw", aliases=["parent"]),
            nestable=dict(required=False, type="bool"),
            content_types=dict(required=False, type="list", elements="str"),
            custom_fields=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    location_type = NautobotDcimModule(module, NB_LOCATION_TYPES)
    location_type.run()


if __name__ == "__main__":  # pragma: no cover
    main()
