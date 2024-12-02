#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: object_metadata
short_description: Creates or removes a object metadata from Nautobot
description:
  - Creates or removes a object metadata from Nautobot
author:
  - Network to Code (@networktocode)
  - Travis Smith (@tsm1th)
version_added: "5.5.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  metadata_type:
    description:
      - The name of the metadata type
    required: true
    type: raw
  assigned_object_type:
    description:
      - The app_label.model for the object in the relationship
    required: true
    type: str
  assigned_object_id:
    description:
      - The UUID of the object in the relationship
    required: true
    type: str
  value:
    description:
      - The value of the metadata
    required: true
    type: str
  scoped_fields:
    description:
      - List of scoped fields, only direct fields on the model
    required: false
    type: list
    elements: str
"""

EXAMPLES = r"""
- name: "Test object metadata creation/deletion"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create object metadata
      networktocode.nautobot.object_metadata:
        url: http://nautobot.local
        token: thisIsMyToken
        metadata_type: "TopSecretInfo"
        assigned_object_type: dcim.device
        assigned_object_id: abcdefgh-0123-abcd-0123-abcdefghijkl
        value: foobar
        scoped_fields:
            - name
    - name: Delete object metadata
      networktocode.nautobot.object_metadata:
        url: http://nautobot.local
        token: thisIsMyToken
        metadata_type: "TopSecretInfo"
        assigned_object_type: dcim.device
        assigned_object_id: abcdefgh-0123-abcd-0123-abcdefghijkl
        value: foobar
        scoped_fields:
            - name
        state: absent
"""

RETURN = r"""
object_metadata:
  description: Serialized object as created/existent/updated/deleted within Nautobot
  returned: always
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.extras import (
    NautobotExtrasModule,
    NB_OBJECT_METADATA,
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
            metadata_type=dict(required=True, type="raw"),
            assigned_object_type=dict(required=True, type="str"),
            assigned_object_id=dict(required=True, type="str"),
            value=dict(required=True, type="str"),
            scoped_fields=dict(required=False, type="list", elements="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    object_metadata = NautobotExtrasModule(module, NB_OBJECT_METADATA)
    object_metadata.run()


if __name__ == "__main__":  # pragma: no cover
    main()
