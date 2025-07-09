#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cloud_network
short_description: Creates or removes cloud network from Nautobot
description:
  - Creates or removes cloud network from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Travis Smith (@tsm1th)
requirements:
  - pynautobot
version_added: "5.4.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the cloud network
    required: true
    type: str
  description:
    description:
      - The description of the cloud network
    required: false
    type: str
  cloud_resource_type:
    description:
      - Required if I(state=present) and the cloud network does not exist yet
    required: false
    type: raw
  cloud_account:
    description:
      - Required if I(state=present) and the cloud network does not exist yet
    required: false
    type: raw
  parent_cloud_network:
    aliases:
      - parent
    description:
      - The parent cloud network this network should be child to
    required: false
    type: raw
  extra_config:
    description:
      - Arbitrary JSON data to define the extra config.
    required: false
    type: dict
"""

EXAMPLES = r"""
---
- name: Create a cloud network
  networktocode.nautobot.cloud_network:
    url: http://nautobot.local
    token: thisIsMyToken
    name: Cisco Quantum Network
    cloud_resource_type: Cisco Quantum Type
    cloud_account: Cisco Quantum Account
    description: A quantum network for Cisco
    state: present

- name: Delete a cloud network
  networktocode.nautobot.cloud_network:
    url: http://nautobot.local
    token: thisIsMyToken
    name: Cisco Quantum Network
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

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.cloud import (
    NB_CLOUD_NETWORKS,
    NautobotCloudModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            cloud_resource_type=dict(required=False, type="raw"),
            cloud_account=dict(required=False, type="raw"),
            parent_cloud_network=dict(required=False, type="raw", aliases=["parent"]),
            extra_config=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    cloud_network = NautobotCloudModule(module, NB_CLOUD_NETWORKS)
    cloud_network.run()


if __name__ == "__main__":  # pragma: no cover
    main()
