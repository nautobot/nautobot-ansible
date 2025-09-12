#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cloud_service_network_assignment
short_description: Creates or removes cloud service network assignments from Nautobot
description:
  - Creates or removes cloud service network assignments from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  id:
    required: false
    type: str
  cloud_network:
    required: true
    type: dict
  cloud_service:
    required: true
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create cloud_service_network_assignment within Nautobot with only required information
      networktocode.nautobot.cloud_service_network_assignment:
        url: http://nautobot.local
        token: thisIsMyToken
        cloud_network: None
        cloud_service: None
        state: present

    - name: Delete cloud_service_network_assignment within nautobot
      networktocode.nautobot.cloud_service_network_assignment:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
cloud_service_network_assignment:
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
    NB_CLOUD_SERVICE_NETWORK_ASSIGNMENTS,
    NautobotCloudModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            cloud_network=dict(required=True, type="dict"),
            cloud_service=dict(required=True, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    cloud_service_network_assignment = NautobotCloudModule(module, NB_CLOUD_SERVICE_NETWORK_ASSIGNMENTS)
    cloud_service_network_assignment.run()


if __name__ == "__main__":  # pragma: no cover
    main()
