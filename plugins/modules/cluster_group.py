#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cluster_group
short_description: Creates or removes cluster groups from Nautobot
description:
  - Creates or removes cluster groups from Nautobot
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
  description:
    required: false
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create cluster_group within Nautobot with only required information
      networktocode.nautobot.cluster_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Cluster_Group
        state: present

    - name: Delete cluster_group within nautobot
      networktocode.nautobot.cluster_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Cluster_Group
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

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import CUSTOM_FIELDS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotVirtualizationModule,
    NB_CLUSTER_GROUPS,
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
            description=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    cluster_group = NautobotVirtualizationModule(module, NB_CLUSTER_GROUPS)
    cluster_group.run()


if __name__ == "__main__":  # pragma: no cover
    main()
