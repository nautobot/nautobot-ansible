#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: device_cluster_assignment
short_description: Creates or removes device cluster assignments from Nautobot
description:
  - Creates or removes device cluster assignments from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Joe Wesch (@joewesch)
requirements:
  - pynautobot
version_added: "6.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
options:
  device:
    description:
      - Device to assign to the cluster
    required: false
    type: raw
  cluster:
    description:
      - Cluster to assign the device to
    required: false
    type: raw
"""

EXAMPLES = r"""
- name: Create a device cluster assignment
  networktocode.nautobot.device_cluster_assignment:
    url: http://nautobot.local
    token: thisIsMyToken
    device: "My Device"
    cluster: "My Cluster"
    state: present

- name: Delete a device cluster assignment
  networktocode.nautobot.device_cluster_assignment:
    url: http://nautobot.local
    token: thisIsMyToken
    device: "My Device"
    cluster: "My Cluster"
    state: absent

- name: Delete a device cluster assignment by id
  networktocode.nautobot.device_cluster_assignment:
    url: http://nautobot.local
    token: thisIsMyToken
    id: 00000000-0000-0000-0000-000000000000
    state: absent
"""

RETURN = r"""
device_cluster_assignment:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating successful operation
  returned: success
  type: str
"""

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NB_DEVICE_CLUSTER_ASSIGNMENTS,
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
            device=dict(required=False, type="raw"),
            cluster=dict(required=False, type="raw"),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    device_cluster_assignment = NautobotDcimModule(module, NB_DEVICE_CLUSTER_ASSIGNMENTS)
    device_cluster_assignment.run()


if __name__ == "__main__":  # pragma: no cover
    main()
