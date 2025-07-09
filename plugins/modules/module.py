#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: module
short_description: Create, update or delete modules within Nautobot
description:
  - Creates, updates or removes modules from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Travis Smith (@tsm1th)
version_added: "5.4.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  module_type:
    description:
      - The module type of the module
    required: true
    type: raw
  serial:
    description:
      - The serial number of the module
    required: false
    type: str
  asset_tag:
    description:
      - The asset tag of the module
    required: false
    type: str
  role:
    description:
      - The role of the module
    required: false
    type: raw
  status:
    description:
      - The status of the module
      - Required if I(state=present) and the device does not exist yet
    required: false
    type: raw
  tenant:
    description:
      - The tenant of the module
    required: false
    type: raw
  location:
    description:
      - The location of the module
    required: false
    type: raw
  parent_module_bay:
    description:
      - The parent module bay of the module
    required: false
    type: raw
"""

EXAMPLES = r"""
- name: Create a module in module bay
  networktocode.nautobot.module:
    url: http://nautobot.local
    token: thisIsMyToken
    module_type: HooverMaxProModel60
    parent_module_bay:
      name: PowerStripTwo
      parent_device: test100
    status: Active
    state: present

- name: Create a module at location
  networktocode.nautobot.module:
    url: http://nautobot.local
    token: thisIsMyToken
    module_type: HooverMaxProModel60
    location:
      name: "Child Test Location"
      parent: "Parent Test Location"
    serial: "654321"
    asset_tag: "123456"
    role: Test Module Role
    status: Active
    tenant: Test Tenant
    state: present

- name: Delete a module
  networktocode.nautobot.module:
    url: http://nautobot.local
    token: thisIsMyToken
    module_type: HooverMaxProModel60
    parent_module_bay:
      name: PowerStripTwo
      parent_device: test100
    state: absent
"""

RETURN = r"""
module:
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
    NB_MODULES,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            module_type=dict(required=True, type="raw"),
            serial=dict(required=False, type="str"),
            asset_tag=dict(required=False, type="str"),
            role=dict(required=False, type="raw"),
            status=dict(required=False, type="raw"),
            tenant=dict(required=False, type="raw"),
            location=dict(required=False, type="raw"),
            parent_module_bay=dict(required=False, type="raw"),
        )
    )

    required_one_of = [
        ("location", "parent_module_bay"),
    ]
    mutually_exclusive = [
        ("location", "parent_module_bay"),
    ]
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=required_one_of,
        mutually_exclusive=mutually_exclusive,
    )

    nb_module = NautobotDcimModule(module, NB_MODULES)
    nb_module.run()


if __name__ == "__main__":  # pragma: no cover
    main()
