#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cluster_group
short_description: Create, update or delete cluster groups within Nautobot
description:
  - Creates, updates or removes cluster groups from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
options:
  name:
    description:
      - The name of the cluster group
      - Required if I(state=present) and the cluster group does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  description:
    description:
      - The description of the cluster group
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
    - name: Create cluster group within Nautobot with only required information
      networktocode.nautobot.cluster_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Cluster Group
        state: present

    - name: Delete cluster within nautobot
      networktocode.nautobot.cluster_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Cluster Group
        state: absent

    - name: Delete cluster group by id
      networktocode.nautobot.cluster_group:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
cluster_group:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import ID_ARG_SPEC, NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.virtualization import (
    NB_CLUSTER_GROUP,
    NautobotVirtualizationModule,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    cluster_group = NautobotVirtualizationModule(module, NB_CLUSTER_GROUP)
    cluster_group.run()


if __name__ == "__main__":  # pragma: no cover
    main()
