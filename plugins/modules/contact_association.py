#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: contact_association
short_description: Creates or removes contact associations from Nautobot
version_added: "5.4.0"
description:
  - Creates or removes contact associations from Nautobot using the /api/extras/contact-associations/ endpoint.
author:
  - Network to Code (@networktocode)
  - Joe Wesch (@joewesch)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  contact:
    description:
      - The contact or team to associate (UUID or dict with identifier).
    required: true
    type: raw
  object_type:
    description:
      - The app_label.model for the object being associated to.
    required: true
    type: str
  object_id:
    description:
      - The UUID of the object being associated to.
    required: true
    type: str
  role:
    description:
      - The role for the association (optional, if applicable).
    required: false
    type: str
"""

EXAMPLES = r"""
- name: Associate a contact to a device
  networktocode.nautobot.contact_association:
    url: http://nautobot.local
    token: thisIsMyToken
    contact:
      id: 01234567-abcd-0123-abcd-012345678901
    object_type: dcim.device
    object_id: abcdefgh-0123-abcd-0123-abcdefghijkl
    role: technical
    state: present

- name: Remove a contact association
  networktocode.nautobot.contact_association:
    url: http://nautobot.local
    token: thisIsMyToken
    contact:
      id: 01234567-abcd-0123-abcd-012345678901
    object_type: dcim.device
    object_id: abcdefgh-0123-abcd-0123-abcdefghijkl
    state: absent
"""

RETURN = r"""
contact_association:
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
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy

NB_CONTACT_ASSOCIATIONS = "contact_associations"

def main():
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            contact=dict(required=True, type="raw"),
            object_type=dict(required=True, type="str"),
            object_id=dict(required=True, type="str"),
            role=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    contact_association = NautobotExtrasModule(module, NB_CONTACT_ASSOCIATIONS)
    contact_association.run()

if __name__ == "__main__":  # pragma: no cover
    main()
