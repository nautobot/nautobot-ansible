#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: platform
short_description: Creates or removes platforms from Nautobot
description:
  - Creates or removes platforms from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  name:
    required: true
    type: str
  network_driver:
    required: false
    type: str
  napalm_driver:
    required: false
    type: str
  napalm_args:
    required: false
    type: str
  description:
    required: false
    type: str
  manufacturer:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create platform within Nautobot with only required information
      networktocode.nautobot.platform:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Platform
        state: present

    - name: Delete platform within nautobot
      networktocode.nautobot.platform:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Platform
        state: absent
"""

RETURN = r"""
platform:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import CUSTOM_FIELDS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_PLATFORMS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            network_driver=dict(required=False, type="str"),
            napalm_driver=dict(required=False, type="str"),
            napalm_args=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            manufacturer=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    platform = NautobotDcimModule(module, NB_PLATFORMS)
    platform.run()


if __name__ == "__main__":  # pragma: no cover
    main()
