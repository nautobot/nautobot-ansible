#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Kulakov Ilya  (@TawR1024)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: service
short_description: Creates or removes service from Nautobot
description:
  - Creates or removes service from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Kulakov Ilya (@TawR1024)
requirements:
  - pynautobot
version_added: "1.0.0"
options:
  url:
    description:
      - URL of the Nautobot instance resolvable by Ansible control host
    required: true
    type: str
  token:
    description:
      - The token created within Nautobot to authorize API access
    required: true
    type: str
  device:
    description:
      - Specifies on which device the service is running
    required: false
    type: raw
  virtual_machine:
    description:
      - Specifies on which virtual machine the service is running
    required: false
    type: raw
  name:
    description:
      - Name of the region to be created
    required: true
    type: str
  ports:
    description:
      - Specifies which ports used by service (Nautobot 2.10 and newer)
    type: list
    elements: int
  protocol:
    description:
      - Specifies which protocol used by service
    required: true
    type: raw
  ipaddresses:
    description:
      - Specifies which IPaddresses to associate with service.
    required: false
    type: raw
  description:
    description:
      - Service description
    required: false
    type: str
  tags:
    description:
      - What tags to add/update
    required: false
    type: list
    elements: raw
  custom_fields:
    description:
      - Must exist in Nautobot and in key/value format
    required: false
    type: dict
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
    type: str
  query_params:
    description:
      - This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined
      - in plugins/module_utils/utils.py and provides control to users on what may make
      - an object unique in their environment.
    required: false
    type: list
    elements: str
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Create nautobot service"
  connection: local
  hosts: all
  gather_facts: False

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
        ipaddresses:
          - address: 127.0.0.1
        tags:
          - prometheus
        state: present

- name: "Delete nautobot service"
  connection: local
  hosts: all
  gather_facts: False

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
    argument_spec.update(
        dict(
            device=dict(required=False, type="raw"),
            virtual_machine=dict(required=False, type="raw"),
            name=dict(required=True, type="str"),
            ports=dict(required=False, type="list", elements="int"),
            protocol=dict(required=True, type="raw"),
            ipaddresses=dict(required=False, type="raw"),
            description=dict(required=False, type="str"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
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
