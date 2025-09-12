#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: service
short_description: Creates or removes services from Nautobot
description:
  - Creates or removes services from Nautobot
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
  ports:
    required: true
    type: list
  name:
    required: true
    type: str
  protocol:
    required: true
    type: str
    choices:
      - "tcp"
      - "udp"
  description:
    required: false
    type: str
  device:
    required: false
    type: dict
  virtual_machine:
    required: false
    type: dict
  ip_addresses:
    required: false
    type: list
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create service within Nautobot with only required information
      networktocode.nautobot.service:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Service
        ports: None
        protocol: tcp
        state: present

    - name: Delete service within nautobot
      networktocode.nautobot.service:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Service
        state: absent
"""

RETURN = r"""
service:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import CUSTOM_FIELDS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import TAGS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotIpamModule,
    NB_SERVICES,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            ports=dict(required=True, type="list"),
            name=dict(required=True, type="str"),
            protocol=dict(
                required=True,
                type="str",
                choices=[
                    "tcp",
                    "udp",
                ],
            ),
            description=dict(required=False, type="str"),
            device=dict(required=False, type="dict"),
            virtual_machine=dict(required=False, type="dict"),
            ip_addresses=dict(required=False, type="list"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    service = NautobotIpamModule(module, NB_SERVICES)
    service.run()


if __name__ == "__main__":  # pragma: no cover
    main()
