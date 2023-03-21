#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2023, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: location
short_description: Creates or removes locations from Nautobot
description:
  - Creates or removes locations from Nautobot
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
      - Name of the location to be created
    required: true
    type: str
  slug:
    description:
      - URL-friendly unique shorthand
    required: false
    type: str
  status:
    description:
      - Status of the location
      - Required if I(state=present) and does not exist yet
    required: false
    type: raw
  description:
    description:
      - Location description
    required: false
    type: str
  location_type:
    description:
      - The type of location
      - Required if I(state=present) and does not exist yet
    required: false
    type: raw
  parent:
    description:
      - The parent location this location should be tied to
    required: false
    type: raw
  site:
    description:
      - The site this location should be tied to
    required: false
    type: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot location module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create location
      networktocode.nautobot.location:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Location
        status: active
        location_type:
          name: My Location Type
        state: present

    - name: Delete location
      networktocode.nautobot.location:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Location
        state: absent

    - name: Create location with all parameters
      networktocode.nautobot.location:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Nested Location
        status: active
        location_type:
          name: My Location Type
        description: My Nested Location Description
        parent:
          name: My Location
        site:
          name: My Site
        state: present
"""

RETURN = r"""
location:
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
    NB_LOCATIONS,
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
            slug=dict(required=False, type="str"),
            status=dict(required=False, type="raw"),
            description=dict(required=False, type="str"),
            location_type=dict(required=False, type="raw"),
            parent=dict(required=False, type="raw"),
            site=dict(required=False, type="raw"),
            custom_fields=dict(required=False, type="dict"),
        )
    )

    required_if = [
        ("state", "present", ["name", "location_type", "status"]),
        ("state", "absent", ["name"]),
    ]

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)

    location = NautobotDcimModule(module, NB_LOCATIONS)
    location.run()


if __name__ == "__main__":  # pragma: no cover
    main()