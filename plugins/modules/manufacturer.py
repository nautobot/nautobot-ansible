#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: manufacturer
short_description: Create or delete manufacturers within Nautobot
description:
  - Creates or removes manufacturers from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  name:
    description:
      - The name of the manufacturer
    required: true
    type: str
    version_added: "3.0.0"
  description:
    description:
      - Applies to the description field for Nautobot Manufacturer
    required: false
    type: str
    version_added: "4.2.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create manufacturer within Nautobot with only required information
      networktocode.nautobot.manufacturer:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Manufacturer
        state: present
        description: The test manufacturer

    - name: Delete manufacturer within nautobot
      networktocode.nautobot.manufacturer:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Manufacturer
        state: absent
"""

RETURN = r"""
manufacturer:
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
    NB_MANUFACTURERS,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    manufacturer = NautobotDcimModule(module, NB_MANUFACTURERS)
    manufacturer.run()


if __name__ == "__main__":  # pragma: no cover
    main()
