#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: relationship_association
short_description: Creates or removes a relationship association from Nautobot
description:
  - Creates or removes a relationship association from Nautobot
author:
  - Network to Code (@networktocode)
  - Joe Wesch (@joewesch)
version_added: "4.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  relationship:
    description:
      - The Relationship UUID to add the association to
    required: true
    type: raw
  source_type:
    description:
      - The app_label.model for the source of the relationship
    required: true
    type: str
  source_id:
    description:
      - The UUID of the source of the relationship
    required: true
    type: str
  destination_type:
    description:
      - The app_label.model for the destination of the relationship
    required: true
    type: str
  destination_id:
    description:
      - The UUID of the destination of the relationship
    required: true
    type: str
"""

EXAMPLES = r"""
- name: "Test relationship association creation/deletion"
  connection: local
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Create relationship association
      networktocode.nautobot.relationship_association:
        url: http://nautobot.local
        token: thisIsMyToken
        relationship: 01234567-abcd-0123-abcd-012345678901
        source_type: dcim.device
        source_id: abcdefgh-0123-abcd-0123-abcdefghijkl
        destination_type: ipam.vrf
        destination_id: 01234567-abcd-0123-abcd-123456789012

    - name: Delete relationship association
      networktocode.nautobot.relationship_association:
        url: http://nautobot.local
        token: thisIsMyToken
        relationship: 01234567-abcd-0123-abcd-012345678901
        source_type: dcim.device
        source_id: abcdefgh-0123-abcd-0123-abcdefghijkl
        destination_type: ipam.vrf
        destination_id: 01234567-abcd-0123-abcd-123456789012
        state: absent
"""

RETURN = r"""
relationship_associations:
  description: Serialized object as created/existent/updated/deleted within Nautobot
  returned: always
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.extras import (
    NB_RELATIONSHIP_ASSOCIATIONS,
    NautobotExtrasModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            relationship=dict(required=True, type="raw"),
            source_type=dict(required=True, type="str"),
            source_id=dict(required=True, type="str"),
            destination_type=dict(required=True, type="str"),
            destination_id=dict(required=True, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    relationship_association = NautobotExtrasModule(module, NB_RELATIONSHIP_ASSOCIATIONS)
    relationship_association.run()


if __name__ == "__main__":  # pragma: no cover
    main()
