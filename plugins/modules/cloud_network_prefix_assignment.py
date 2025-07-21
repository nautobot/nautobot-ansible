#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cloud_network_prefix_assignment
short_description: Creates or removes cloud network to prefix association from Nautobot
description:
  - Creates or removes cloud network to prefix association from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Travis Smith (@tsm1th)
requirements:
  - pynautobot
version_added: "5.4.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
options:
  cloud_network:
    description:
      - Cloud network to associate with a prefix.
      - Required if I(state=present) and the cloud network to prefix assignment does not exist yet
    required: false
    type: raw
  cloud_prefix:
    aliases:
      - prefix
    description:
      - Prefix to associate with a cloud network.
      - Required if I(state=present) and the cloud network to prefix assignment does not exist yet
    required: false
    type: raw
"""

EXAMPLES = r"""
---
- name: Create a cloud network to prefix assignment
  networktocode.nautobot.cloud_network_prefix_assignment:
    url: http://nautobot.local
    token: thisIsMyToken
    cloud_network: Cisco Quantum Network
    cloud_prefix: 10.1.198.0/23
    state: present

- name: Delete a cloud network to prefix assignment
  networktocode.nautobot.cloud_network_prefix_assignment:
    url: http://nautobot.local
    token: thisIsMyToken
    cloud_network: Cisco Quantum Network
    cloud_prefix: 10.1.198.0/23
    state: absent

- name: Delete a cloud network to prefix assignment by id
  networktocode.nautobot.cloud_network_prefix_assignment:
    url: http://nautobot.local
    token: thisIsMyToken
    id: 00000000-0000-0000-0000-000000000000
    state: absent
"""

RETURN = r"""
cloud_network_prefix_assignment:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.cloud import (
    NB_CLOUD_NETWORK_PREFIX_ASSIGNMENTS,
    NautobotCloudModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import ID_ARG_SPEC, NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(
        dict(
            cloud_network=dict(required=False, type="raw"),
            cloud_prefix=dict(required=False, type="raw", aliases=["prefix"]),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    cloud_network_prefix_assignment = NautobotCloudModule(module, NB_CLOUD_NETWORK_PREFIX_ASSIGNMENTS)
    cloud_network_prefix_assignment.run()


if __name__ == "__main__":  # pragma: no cover
    main()
