#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cluster_type
short_description: Create, update or delete cluster types within Nautobot
description:
  - Creates, updates or removes cluster types from Nautobot
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
      - The name of the cluster type
    required: true
    type: str
    version_added: "3.0.0"
  description:
    description:
      - The description of the cluster type
    required: false
    type: str
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create cluster type within Nautobot with only required information
      networktocode.nautobot.cluster_type:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Cluster Type
        state: present

    - name: Delete cluster within nautobot
      networktocode.nautobot.cluster_type:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Cluster Type
        state: absent
"""

RETURN = r"""
cluster_type:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.virtualization import (
    NautobotVirtualizationModule,
    NB_CLUSTER_TYPE,
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
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    cluster_type = NautobotVirtualizationModule(module, NB_CLUSTER_TYPE)
    cluster_type.run()


if __name__ == "__main__":  # pragma: no cover
    main()
