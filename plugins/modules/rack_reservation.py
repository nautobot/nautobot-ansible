#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: rack_reservation
short_description: Creates or removes rack reservations from Nautobot
description:
  - Creates or removes rack reservations from Nautobot
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
  units:
    required: true
    type: str
  description:
    required: true
    type: str
  rack:
    required: true
    type: dict
  tenant:
    required: false
    type: dict
  user:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create rack reservation within Nautobot with only required information
      networktocode.nautobot.rack_reservation:
        url: http://nautobot.local
        token: thisIsMyToken
        units: None
        description: "Test description"
        rack: None
        state: present

    - name: Delete rack_reservation within nautobot
      networktocode.nautobot.rack_reservation:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
rack_reservation:
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
    NB_RACK_RESERVATIONS,
    NautobotDcimModule,
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
            units=dict(required=True, type="str"),
            description=dict(required=True, type="str"),
            rack=dict(required=True, type="dict"),
            tenant=dict(required=False, type="dict"),
            user=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    rack_reservation = NautobotDcimModule(module, NB_RACK_RESERVATIONS)
    rack_reservation.run()


if __name__ == "__main__":  # pragma: no cover
    main()
