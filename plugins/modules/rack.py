#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rack
short_description: Create, update or delete racks within Nautobot
description:
  - Creates, updates or removes racks from Nautobot.
notes:
  - Tags should be defined as a YAML list.
  - This should be ran with connection C(local) and hosts C(localhost).
  - The module supports C(check_mode).
author:
  - NMikhail Yohman (@FragmentedPacket)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the rack.
      - Required if I(state=present) and the rack does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  facility_id:
    description:
      - The unique rack ID assigned by the facility.
    required: false
    type: str
    version_added: "3.0.0"
  location:
    description:
      - The location the rack is located in
      - Required if I(state=present) and the rack does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  rack_group:
    description:
      - The rack group the rack will be associated to.
    required: false
    type: raw
    version_added: "3.0.0"
  tenant:
    description:
      - The tenant that the device will be assigned to.
    required: false
    type: raw
    version_added: "3.0.0"
  status:
    description:
      - The status of the rack
      - Required if I(state=present) and does not exist yet.
    required: false
    type: raw
    version_added: "3.0.0"
  role:
    description:
      - The rack role the rack will be associated to.
    required: false
    type: raw
    version_added: "3.0.0"
  serial:
    description:
      - Serial number of the rack.
    required: false
    type: str
    version_added: "3.0.0"
  asset_tag:
    description:
      - Asset tag that is associated to the rack.
    required: false
    type: str
    version_added: "3.0.0"
  type:
    description:
      - The type of rack.
    required: false
    type: str
    version_added: "3.0.0"
  width:
    description:
      - The rail-to-rail width.
    choices:
      - 10
      - 19
      - 21
      - 23
    required: false
    type: int
    version_added: "3.0.0"
  u_height:
    description:
      - The height of the rack in rack units.
    required: false
    type: int
    version_added: "3.0.0"
  desc_units:
    description:
      - Rack units will be numbered top-to-bottom.
    required: false
    type: bool
    version_added: "3.0.0"
  outer_width:
    description:
      - The outer width of the rack.
    required: false
    type: int
    version_added: "3.0.0"
  outer_depth:
    description:
      - The outer depth of the rack.
    required: false
    type: int
    version_added: "3.0.0"
  outer_unit:
    description:
      - Whether the rack unit is in Millimeters or Inches and is I(required) if outer_width/outer_depth is specified.
    choices:
      - Millimeters
      - Inches
    required: false
    type: str
    version_added: "3.0.0"
  comments:
    description:
      - Comments that may include additional information in regards to the rack.
    required: false
    type: str
    version_added: "3.0.0"
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
        name: Test rack
        location:
          name: My Location
          parent: Parent Location
        status: active
        state: present

    - name: Delete rack within nautobot
      networktocode.nautobot.rack:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rack
        state: absent

    - name: Delete rack by id
      networktocode.nautobot.rack:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
rack:
  description: Serialized object as created or already existent within Nautobot.
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved.
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
            name=dict(required=False, type="str"),
            facility_id=dict(required=False, type="str"),
            location=dict(required=False, type="raw"),
            rack_group=dict(required=False, type="raw"),
            tenant=dict(required=False, type="raw"),
            status=dict(required=False, type="raw"),
            role=dict(required=False, type="raw"),
            serial=dict(required=False, type="str"),
            asset_tag=dict(required=False, type="str"),
            type=dict(required=False, type="str"),
            width=dict(required=False, type="int", choices=[10, 19, 21, 23]),
            u_height=dict(required=False, type="int"),
            desc_units=dict(required=False, type="bool"),
            outer_width=dict(required=False, type="int"),
            outer_depth=dict(required=False, type="int"),
            outer_unit=dict(
                required=False,
                type="str",
                choices=["Millimeters", "Inches"],
            ),
            comments=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    rack = NautobotDcimModule(module, NB_RACKS)
    rack.run()


if __name__ == "__main__":  # pragma: no cover
    main()
