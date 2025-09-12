#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rack
short_description: Creates or removes racks from Nautobot
description:
  - Creates or removes racks from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  name:
    required: true
    type: str
  facility_id:
    required: false
    type: str
  serial:
    required: false
    type: str
  asset_tag:
    required: false
    type: str
  type:
    required: false
    type: str
    choices:
      - "2-post-frame"
      - "4-post-frame"
      - "4-post-cabinet"
      - "wall-frame"
      - "wall-frame-vertical"
      - "wall-cabinet"
      - "wall-cabinet-vertical"
      - "other"
  width:
    required: false
    type: str
  u_height:
    required: false
    type: int
  desc_units:
    required: false
    type: bool
  outer_width:
    required: false
    type: int
  outer_depth:
    required: false
    type: int
  outer_unit:
    required: false
    type: str
    choices:
      - "mm"
      - "in"
  comments:
    required: false
    type: str
  status:
    required: true
    type: str
  role:
    required: false
    type: dict
  location:
    required: true
    type: dict
  rack_group:
    required: false
    type: dict
  tenant:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create rack within Nautobot with only required information
      networktocode.nautobot.rack:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rack
        status: "Active"
        location: None
        state: present

    - name: Delete rack within nautobot
      networktocode.nautobot.rack:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rack
        state: absent
"""

RETURN = r"""
rack:
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
    NB_RACKS,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            facility_id=dict(required=False, type="str"),
            serial=dict(required=False, type="str"),
            asset_tag=dict(required=False, type="str"),
            type=dict(
                required=False,
                type="str",
                choices=[
                    "2-post-frame",
                    "4-post-frame",
                    "4-post-cabinet",
                    "wall-frame",
                    "wall-frame-vertical",
                    "wall-cabinet",
                    "wall-cabinet-vertical",
                    "other",
                ],
            ),
            width=dict(required=False, type="str"),
            u_height=dict(required=False, type="int"),
            desc_units=dict(required=False, type="bool"),
            outer_width=dict(required=False, type="int"),
            outer_depth=dict(required=False, type="int"),
            outer_unit=dict(
                required=False,
                type="str",
                choices=[
                    "mm",
                    "in",
                ],
            ),
            comments=dict(required=False, type="str"),
            status=dict(required=True, type="str"),
            role=dict(required=False, type="dict"),
            location=dict(required=True, type="dict"),
            rack_group=dict(required=False, type="dict"),
            tenant=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    rack = NautobotDcimModule(module, NB_RACKS)
    rack.run()


if __name__ == "__main__":  # pragma: no cover
    main()
