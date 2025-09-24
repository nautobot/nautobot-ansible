#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: virtual_device_context
short_description: Create, update or delete virtual device contexts within Nautobot
description:
  - Creates, updates or removes virtual device contexts from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
  - This module requires Nautobot 2.4 or later
author:
  - Joe Wesch (@joewesch)
requirements:
  - pynautobot
version_added: "5.16.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the virtual device context
      - Required if I(state=present) and the virtual device context does not exist yet
    required: false
    type: str
  description:
    description:
      - The description of the virtual device context
    required: false
    type: str
  identifier:
    description:
      - Unique identifier provided by the platform being virtualized
    required: false
    type: int
  device:
    description:
      - The device that the virtual device context is associated with
      - Required if I(state=present) and the virtual device context does not exist yet
    required: false
    type: raw
  status:
    description:
      - The status of the virtual device context
      - Required if I(state=present) and the virtual device context does not exist yet
    required: false
    type: raw
  role:
    description:
      - The role of the virtual device context
    required: false
    type: raw
  primary_ip4:
    description:
      - The primary IPv4 address of the virtual device context
    required: false
    type: raw
  primary_ip6:
    description:
      - The primary IPv6 address of the virtual device context
    required: false
    type: raw
  tenant:
    description:
      - The tenant that the virtual device context is associated with
    required: false
    type: raw
"""

EXAMPLES = r"""
- name: Create a virtual device context
  networktocode.nautobot.virtual_device_context:
    url: http://nautobot.local
    token: thisIsMyToken
    name: "My Virtual Device Context"
    device: "My Device"
    status: "Active"
    state: present

- name: Delete a virtual device context
  networktocode.nautobot.virtual_device_context:
    url: http://nautobot.local
    token: thisIsMyToken
    name: "My Virtual Device Context"
    state: absent

- name: Delete a virtual device context by id
  networktocode.nautobot.virtual_device_context:
    url: http://nautobot.local
    token: thisIsMyToken
    id: 00000000-0000-0000-0000-000000000000
    state: absent
"""

RETURN = r"""
virtual_device_context:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating successful operation
  returned: success
  type: str
"""

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NB_VIRTUAL_DEVICE_CONTEXTS,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            identifier=dict(required=False, type="int"),
            device=dict(required=False, type="raw"),
            status=dict(required=False, type="raw"),
            role=dict(required=False, type="raw"),
            primary_ip4=dict(required=False, type="raw"),
            primary_ip6=dict(required=False, type="raw"),
            tenant=dict(required=False, type="raw"),
        )
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    virtual_device_context = NautobotDcimModule(module, NB_VIRTUAL_DEVICE_CONTEXTS)
    virtual_device_context.run()


if __name__ == "__main__":  # pragma: no cover
    main()
