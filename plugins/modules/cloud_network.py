#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cloud_network
short_description: Creates or removes cloud networks from Nautobot
description:
  - Creates or removes cloud networks from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  extra_config:
    required: false
    type: str
  name:
    required: true
    type: str
  description:
    required: false
    type: str
  cloud_resource_type:
    required: true
    type: dict
  cloud_account:
    required: true
    type: dict
  parent:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create cloud_network within Nautobot with only required information
      networktocode.nautobot.cloud_network:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Cloud_Network
        cloud_resource_type: None
        cloud_account: None
        state: present

    - name: Delete cloud_network within nautobot
      networktocode.nautobot.cloud_network:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Cloud_Network
        state: absent
"""

RETURN = r"""
cloud_network:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import TAGS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotCloudModule,
    NB_CLOUD_NETWORKS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            extra_config=dict(required=False, type="str"),
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            cloud_resource_type=dict(required=True, type="dict"),
            cloud_account=dict(required=True, type="dict"),
            parent=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    cloud_network = NautobotCloudModule(module, NB_CLOUD_NETWORKS)
    cloud_network.run()


if __name__ == "__main__":  # pragma: no cover
    main()
