#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: static_group_association
short_description: Creates or removes a static group association from Nautobot
description:
  - Creates or removes a static group association from Nautobot
author:
  - Network to Code (@networktocode)
  - Travis Smith (@tsm1th)
version_added: "5.5.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.custom_fields
options:
  dynamic_group:
    description:
      - The dynamic group to add the association to
    required: true
    type: raw
  associated_object_type:
    description:
      - The app_label.model for the object in the relationship
    required: true
    type: str
  associated_object_id:
    description:
      - The UUID of the object in the relationship
    required: true
    type: str
"""

EXAMPLES = r"""
- name: "Test static group association creation/deletion"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create static group association
      networktocode.nautobot.static_group_association:
        url: http://nautobot.local
        token: thisIsMyToken
        dynamic_group: 01234567-abcd-0123-abcd-012345678901
        associated_object_type: dcim.device
        associated_object_id: abcdefgh-0123-abcd-0123-abcdefghijkl

    - name: Delete static group association
      networktocode.nautobot.static_group_association:
        url: http://nautobot.local
        token: thisIsMyToken
        dynamic_group: 01234567-abcd-0123-abcd-012345678901
        associated_object_type: dcim.device
        associated_object_id: abcdefgh-0123-abcd-0123-abcdefghijkl
        state: absent
"""

RETURN = r"""
static_group_association:
  description: Serialized object as created/existent/updated/deleted within Nautobot
  returned: always
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
    CUSTOM_FIELDS_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.extras import (
    NautobotExtrasModule,
    NB_STATIC_GROUP_ASSOCIATIONS,
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
            dynamic_group=dict(required=True, type="raw"),
            associated_object_type=dict(required=True, type="str"),
            associated_object_id=dict(required=True, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    static_group_association = NautobotExtrasModule(module, NB_STATIC_GROUP_ASSOCIATIONS)
    static_group_association.run()


if __name__ == "__main__":  # pragma: no cover
    main()