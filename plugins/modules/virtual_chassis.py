#!/usr/bin/python
# -*- coding: utf-8 -*-
# © 2020 Nokia
# Licensed under the GNU General Public License v3.0 only
# SPDX-License-Identifier: GPL-3.0-only

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: virtual_chassis
short_description: Create, update or delete virtual chassis within Nautobot
description:
  - Creates, updates or removes virtual chassis from Nautobot
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
  name:
    description:
      - Name
    required: true
    type: str
    version_added: "3.0.0"
  master:
    description:
      - The master device the virtual chassis is attached to
    required: false
    type: raw
    version_added: "3.0.0"
  domain:
    description:
      - domain of the virtual chassis
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
    - name: Create virtual chassis within Nautobot with only required information
      networktocode.nautobot.virtual_chassis:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "Virtual Chassis 1"
        state: present

    - name: Update virtual chassis with other fields
      networktocode.nautobot.virtual_chassis:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "Virtual Chassis 1"
        master: Test Device
        domain: Domain Text
        state: present

    - name: Delete virtual chassis within nautobot
      networktocode.nautobot.virtual_chassis:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "Virtual Chassis 1"
        state: absent
"""

RETURN = r"""
virtual_chassis:
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
    NB_VIRTUAL_CHASSIS,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            master=dict(required=False, type="raw"),
            domain=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    virtual_chassis = NautobotDcimModule(module, NB_VIRTUAL_CHASSIS)
    virtual_chassis.run()


if __name__ == "__main__":  # pragma: no cover
    main()
