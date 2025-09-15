#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: location
short_description: Creates or removes locations from Nautobot
description:
  - Creates or removes locations from Nautobot
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
  time_zone:
    required: false
    type: str
  name:
    required: true
    type: str
  description:
    required: false
    type: str
  facility:
    required: false
    type: str
  asn:
    required: false
    type: int
  physical_address:
    required: false
    type: str
  shipping_address:
    required: false
    type: str
  latitude:
    required: false
    type: str
  longitude:
    required: false
    type: str
  contact_name:
    required: false
    type: str
  contact_phone:
    required: false
    type: str
  contact_email:
    required: false
    type: str
  comments:
    required: false
    type: str
  parent:
    required: false
    type: dict
  location_type:
    required: true
    type: dict
  status:
    required: true
    type: str
  tenant:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create location within Nautobot with only required information
      networktocode.nautobot.location:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Location
        location_type: None
        status: "Active"
        state: present

    - name: Delete location within nautobot
      networktocode.nautobot.location:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Location
        state: absent
"""

RETURN = r"""
location:
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
    NB_LOCATIONS,
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
            time_zone=dict(required=False, type="str"),
            name=dict(required=True, type="str"),
            description=dict(required=False, type="str"),
            facility=dict(required=False, type="str"),
            asn=dict(required=False, type="int"),
            physical_address=dict(required=False, type="str"),
            shipping_address=dict(required=False, type="str"),
            latitude=dict(required=False, type="str"),
            longitude=dict(required=False, type="str"),
            contact_name=dict(required=False, type="str"),
            contact_phone=dict(required=False, type="str"),
            contact_email=dict(required=False, type="str"),
            comments=dict(required=False, type="str"),
            parent=dict(required=False, type="dict"),
            location_type=dict(required=True, type="dict"),
            status=dict(required=True, type="str"),
            tenant=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    location = NautobotDcimModule(module, NB_LOCATIONS)
    location.run()


if __name__ == "__main__":  # pragma: no cover
    main()
