#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: power_panel
short_description: Create, update or delete power panels within Nautobot
description:
  - Creates, updates or removes power panels from Nautobot
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
  location:
    description:
      - The location the power panel is located in
      - Required if I(state=present) and the power panel does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  rack_group:
    description:
      - The rack group the power panel is assigned to
    required: false
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - The name of the power panel
      - Required if I(state=present) and the power panel does not exist yet
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
    - name: Create power panel within Nautobot with only required information
      networktocode.nautobot.power_panel:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Panel
        location: My Location
        state: present

    - name: Update power panel with other fields
      networktocode.nautobot.power_panel:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Panel
        location:
          name: My Location
          parent: Parent Location
        rack_group: Test Rack Group
        state: present

    - name: Delete power panel within nautobot
      networktocode.nautobot.power_panel:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Power Panel
        location:
          name: My Location
          parent: Parent Location
        state: absent

    - name: Delete power panel by id
      networktocode.nautobot.power_panel:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
power_panel:
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
    NB_POWER_PANELS,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(
        dict(
            location=dict(required=False, type="raw"),
            rack_group=dict(required=False, type="raw"),
            name=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    power_panel = NautobotDcimModule(module, NB_POWER_PANELS)
    power_panel.run()


if __name__ == "__main__":  # pragma: no cover
    main()
