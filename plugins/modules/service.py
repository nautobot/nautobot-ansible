#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Kulakov Ilya  (@TawR1024)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: service
short_description: Creates or removes service from Nautobot
description:
  - Creates or removes service from Nautobot.
notes:
  - This should be ran with connection C(local) and hosts C(localhost).
  - The module supports C(check_mode).
author:
  - Kulakov Ilya (@TawR1024)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  device:
    description:
      - Specifies on which device the service is running.
    required: false
    type: raw
    version_added: "3.0.0"
  virtual_machine:
    description:
      - Specifies on which virtual machine the service is running.
    required: false
    type: raw
    version_added: "3.0.0"
  name:
    description:
      - Name of the region to be created.
    required: true
    type: str
    version_added: "3.0.0"
  ports:
    description:
      - Specifies which ports used by service (Nautobot 2.10 and newer).
    type: list
    elements: int
    version_added: "3.0.0"
  protocol:
    description:
      - Specifies which protocol used by service.
    required: true
    type: raw
    version_added: "3.0.0"
  ip_addresses:
    description:
      - Specifies which IPaddresses to associate with service.
    required: false
    type: raw
    version_added: "3.0.0"
  description:
    description:
      - Service description.
    required: false
    type: str
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Create nautobot service"
  connection: local
  hosts: all
  gather_facts: false

  tasks:
    - name: Create service
      networktocode.nautobot.service:
        url: url
        token: token
        device: Test666
        name: node-exporter
        ports:
          - 9100
        protocol: TCP
        ip_addresses:
          - address: 127.0.0.1
        tags:
          - prometheus
        state: present

- name: "Delete nautobot service"
  connection: local
  hosts: all
  gather_facts: false

  tasks:
    - name: Delete service
      networktocode.nautobot.service:
        url: url
        token: token
        device: Test666
        name: node-exporter
        ports:
          - 9100
        protocol: TCP
        state: absent
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
    CUSTOM_FIELDS_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
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
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            device=dict(required=False, type="raw"),
            virtual_machine=dict(required=False, type="raw"),
            name=dict(required=True, type="str"),
            ports=dict(required=False, type="list", elements="int"),
            protocol=dict(required=True, type="raw"),
            ip_addresses=dict(required=False, type="raw"),
            description=dict(required=False, type="str"),
        )
    )
    required_one_of = [["device", "virtual_machine"]]

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_one_of=required_one_of,
    )

    service = NautobotIpamModule(module, NB_SERVICES)

    # Run the normal run() method
    service.run()


if __name__ == "__main__":  # pragma: no cover
    main()
