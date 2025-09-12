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
description:
  - Creates or removes contact associations from Nautobot
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
  associated_object_type:
    required: true
    type: str
  associated_object_id:
    required: true
    type: str
  contact:
    required: false
    type: dict
  team:
    required: false
    type: dict
  role:
    required: true
    type: dict
  status:
    required: true
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create contact_association within Nautobot with only required information
      networktocode.nautobot.contact_association:
        url: http://nautobot.local
        token: thisIsMyToken
        associated_object_type: "Test associated_object_type"
        associated_object_id: "Test associated_object_id"
        role: None
        status: "Active"
        state: present

    - name: Delete contact_association within nautobot
      networktocode.nautobot.contact_association:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
contact_association:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NB_CONTACT_ASSOCIATIONS,
    NautobotExtrasModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            associated_object_type=dict(required=True, type="str"),
            associated_object_id=dict(required=True, type="str"),
            contact=dict(required=False, type="dict"),
            team=dict(required=False, type="dict"),
            role=dict(required=True, type="dict"),
            status=dict(required=True, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    contact_association = NautobotExtrasModule(module, NB_CONTACT_ASSOCIATIONS)
    contact_association.run()


if __name__ == "__main__":  # pragma: no cover
    main()
