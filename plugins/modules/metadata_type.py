#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: metadata_type
short_description: Creates or removes metadata types from Nautobot
description:
  - Creates or removes metadata types from Nautobot
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
  content_types:
    required: true
    type: list
  name:
    required: true
    type: str
  description:
    required: false
    type: str
  data_type:
    required: true
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create metadata type within Nautobot with only required information
      networktocode.nautobot.metadata_type:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Metadata Type
        content_types: None
        data_type: None
        state: present

    - name: Delete metadata_type within nautobot
      networktocode.nautobot.metadata_type:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Metadata Type
        state: absent
"""

RETURN = r"""
metadata_type:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.extras import (
    NB_METADATA_TYPES,
    NautobotExtrasModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            content_types=dict(required=True, type="list"),
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            data_type=dict(required=True, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    metadata_type = NautobotExtrasModule(module, NB_METADATA_TYPES)
    metadata_type.run()


if __name__ == "__main__":  # pragma: no cover
    main()
