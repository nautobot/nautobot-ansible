#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Pavel Korovin (@pkorovin) <p@tristero.se>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: tag
short_description: Creates or removes tags from Nautobot
description:
  - Creates or removes tags from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Pavel Korovin (@pkorovin)
requirements:
  - pynautobot
version_added: "1.0.0"
options:
  api_version:
    description:
      - API Version Nautobot REST API
    required: false
    type: str
    version_added: "4.1.0"
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
  name:
    description:
      - Tag name
    required: true
    type: str
    version_added: "3.0.0"
  slug:
    description:
      - The slugified version of the name or custom slug.
      - This is auto-generated following Nautobot rules if not provided
    required: false
    type: str
    version_added: "3.0.0"
  color:
    description:
      - Tag color
    required: false
    type: str
    version_added: "3.0.0"
  description:
    description:
      - Tag description
    required: false
    type: str
    version_added: "3.0.0"
  content_types:
    description:
      - Tags content type(s). These match app.endpoint and the endpoint is singular.
      - e.g. dcim.device, ipam.ipaddress (more can be found in the examples)
      - Requires `api_version >= 1.3`
    required: false
    type: list
    elements: str
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
    version_added: "3.0.0"
  validate_certs:
    description:
      - |
        If C(no), SSL certificates will not be validated.
        This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test tags creation/deletion"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create tags
      networktocode.nautobot.tag:
        url: http://nautobot.local
        token: thisIsMyToken
        api_version: "1.3"
        name: "{{ item.name }}"
        description: "{{ item.description }}"
        content_types:
          - circuits.circuit
          - circuits.circuit termination
          - circuits.provider
          - circuits.provider network
          - dcim.cable
          - dcim.console port
          - dcim.console server port
          - dcim.device
          - dcim.device bay
          - dcim.device type
          - dcim.front port
          - dcim.interface
          - dcim.inventory item
          - dcim.power feed
          - dcim.power outlet
          - dcim.power panel
          - dcim.power port
          - dcim.rack
          - dcim.rack reservation
          - dcim.rear port
          - dcim.site
          - dcim.virtual chassis
          - extras.Git repository
          - extras.job
          - extras.secret
          - ipam.aggregate
          - ipam.IP address
          - ipam.prefix
          - ipam.route target
          - ipam.service
          - ipam.VLAN
          - ipam.VRF
          - tenancy.tenant
          - virtualization.cluster
          - virtualization.virtual machine
          - virtualization.VM interface
      loop:
        - { name: mgmt, description: "management" }
        - { name: tun, description: "tunnel" }
      

    - name: Delete tags
      networktocode.nautobot.tag:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "{{ item }}"
        state: absent
      loop:
        - mgmt
        - tun
"""

RETURN = r"""
tags:
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
    NB_TAGS,
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
            name=dict(required=True, type="str"),
            color=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            slug=dict(required=False, type="str"),
            content_types=dict(required=False, type="list", elements="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    tag = NautobotExtrasModule(module, NB_TAGS)
    tag.run()


if __name__ == "__main__":  # pragma: no cover
    main()
