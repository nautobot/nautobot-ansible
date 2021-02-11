#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.0",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: netbox_status
short_description: Creates or removes status from Nautobot
description:
  - Creates or removes status from Nautobot
notes:
  - Status should be defined as a YAML list
author:
  - Network to Code, LLC (networktocode)
  - Mikhail Yohman (@fragmentedpacket)
  - Josh VanDeraa (@jvanaderaa)
requirements:
  - pynautobot
version_added: "1.0.0"
options:
  netbox_url:
    description:
      - URL of the Netbox instance resolvable by Ansible control host
    required: false
    type: str
  netbox_token:
    description:
      - The token created within Netbox to authorize API access
    required: false
    type: str
  data:
    type: dict
    description:
      - Defines the tag configuration
    suboptions:
      name:
        description:
          - Status name
        required: true
        type: str
      slug:
        description:
          - The slugified version of the name or custom slug.
          - This is auto-generated following Nautobot rules if not provided
        required: false
        type: str
      color:
        description:
          - Status color
        required: false
        type: str
      content_types:
        description:
          - Status content type(s)
        required: true
        type: list
        elements: str
        choices:
          - dcim.device
        default:
          - dcim.device
    required: true
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
    type: str
  validate_certs:
    description:
      - |
        If C(no), SSL certificates will not be validated.
        This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test status creation/deletion"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create status
      netbox_status:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: "{{ item.name }}"
          content_types:
            - dcim.device
          color: 01bea3

    - name: Delete status
      netbox_status:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: "ansible_status"
          content_types:
            - dcim.device
          color: 01bea3
        state: absent
"""

RETURN = r"""
statuses:
  description: Serialized object as created/existent/updated/deleted within Nautobot
  returned: always
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.netbox.netbox.plugins.module_utils.netbox_utils import (
    NetboxAnsibleModule,
    NETBOX_ARG_SPEC,
)
from ansible_collections.netbox.netbox.plugins.module_utils.netbox_extras import (
    NetboxExtrasModule,
    NB_STATUS,
)
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NETBOX_ARG_SPEC)
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    name=dict(required=True, type="str"),
                    content_types=dict(required=True, type="list", elements="str"),
                    color=dict(required=False, type="str"),
                    slug=dict(required=False, type="str"),
                ),
            ),
        )
    )

    required_if = [("state", "present", ["name"]), ("state", "absent", ["name"])]

    module = NetboxAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    netbox_status = NetboxExtrasModule(module, NB_STATUS)
    netbox_status.run()


if __name__ == "__main__":  # pragma: no cover
    main()
