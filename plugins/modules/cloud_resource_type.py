#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: cloud_resource_type
short_description: Creates or removes cloud resource type from Nautobot
description:
  - Creates or removes cloud resource type from Nautobot
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
      - The name of the cloud resource type
    required: true
    type: str
  description:
    description:
      - The description of the cloud resource type
    required: false
    type: str
  cloud_provider:
    aliases:
      - provider
    description:
      - Required if I(state=present) and the cloud resource type does not exist yet
    required: false
    type: raw
  content_types:
    description:
      - Required if I(state=present) and the cloud resource type does not exist yet
      - Cloud Resource Type content type(s). These match app.endpoint and the endpoint is singular.
      - cloud.cloudnetwork, cloud.cloudservice
    type: list
    elements: str
  config_schema:
    description:
      - Arbitrary JSON data to define the config schema.
    required: false
    type: dict
"""

EXAMPLES = r"""
---
- name: Create a cloud resource type
  networktocode.nautobot.cloud_resource_type:
    url: http://nautobot.local
    token: thisIsMyToken
    name: Cisco Quantum Network
    provider: Cisco
    content_types:
      - "cloud.cloudnetwork"
    state: present

- name: Delete a cloud resource type
  networktocode.nautobot.cloud_resource_type:
    url: http://nautobot.local
    token: thisIsMyToken
    name: Cisco Quantum Network
    state: absent
"""

RETURN = r"""
cloud_resource_type:
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
    NB_CLOUD_RESOURCE_TYPES,
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
            cloud_provider=dict(required=False, type="raw", aliases=["provider"]),
            content_types=dict(required=False, type="list", elements="str"),
            config_schema=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    cloud_resource_type = NautobotCloudModule(module, NB_CLOUD_RESOURCE_TYPES)
    cloud_resource_type.run()


if __name__ == "__main__":  # pragma: no cover
    main()
