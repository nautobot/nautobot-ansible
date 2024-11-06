#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cloud_service
short_description: Creates or removes cloud service from Nautobot
description:
  - Creates or removes cloud service from Nautobot
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
      - The name of the cloud service
    required: true
    type: str
  description:
    description:
      - The description of the cloud service
    required: false
    type: str
  cloud_resource_type:
    description:
      - Required if I(state=present) and the cloud service does not exist yet
    required: false
    type: raw
  cloud_account:
    description:
      - A cloud account for this service.
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
- name: Create a cloud service
  networktocode.nautobot.cloud_service:
    url: http://nautobot.local
    token: thisIsMyToken
    name: Cisco Quantum Service
    cloud_resource_type: Cisco Quantum Type
    cloud_account: Cisco Quantum Account
    description: A quantum service for Cisco
    state: present

- name: Delete a cloud service
  networktocode.nautobot.cloud_service:
    url: http://nautobot.local
    token: thisIsMyToken
    name: Cisco Quantum Service
    state: absent
"""

RETURN = r"""
cloud_service:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
    CUSTOM_FIELDS_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.cloud import (
    NautobotCloudModule,
    NB_CLOUD_SERVICES,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
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
            extra_config=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    cloud_service = NautobotCloudModule(module, NB_CLOUD_SERVICES)
    cloud_service.run()


if __name__ == "__main__":  # pragma: no cover
    main()
