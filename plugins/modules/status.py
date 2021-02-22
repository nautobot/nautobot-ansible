#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.0",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: status
short_description: Creates or removes status from Nautobot
description:
  - Creates or removes status from Nautobot
notes:
  - Status should be defined as a YAML list
author:
  - Network to Code (@networktocode)
  - Josh VanDeraa (@jvanaderaa)
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
      description:
        description:
          - The description for the status
        required: false
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
          - Status content type(s). These match app.endpoint and the endpoint is singular.
          - e.g. dcim.device, ipam.ipaddress (more can be found in the examples)
        required: false
        type: list
        elements: str
    required: true
  query_params:
    description:
      - This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined
      - in plugins/module_utils/utils.py and provides control to users on what may make
      - an object unique in their environment.
    required: false
    type: list
    elements: str
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
      networktocode.nautobot.status:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: "ansible_status"
          description: "Status if provisioned by Ansible"
          content_types:
            - dcim.device
            - dcim.cable
            - dcim.powerfeed
            - dcim.rack
            - dcim.site
            - circuits.circuit
            - virtualization.virtualmachine
            - ipam.prefix
            - ipam.ipaddress
            - ipam.vlan
          color: 01bea3

    - name: Delete status
      networktocode.nautobot.status:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: "ansible_status"
          content_types:
            - dcim.device
            - dcim.cable
            - dcim.powerfeed
            - dcim.rack
            - dcim.site
            - circuits.circuit
            - virtualization.virtualmachine
            - ipam.prefix
            - ipam.ipaddress
            - ipam.vlan
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

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NautobotAnsibleModule,
    NAUTOBOT_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.extras import (
    NautobotExtrasModule,
    NB_STATUS,
)
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    name=dict(required=True, type="str"),
                    content_types=dict(required=False, type="list", elements="str"),
                    color=dict(required=False, type="str"),
                    description=dict(required=False, type="str"),
                    slug=dict(required=False, type="str"),
                ),
            ),
        )
    )

    required_if = [
        ("state", "present", ["name", "content_types"]),
        ("state", "absent", ["name"]),
    ]

    module = NautobotAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    status = NautobotExtrasModule(module, NB_STATUS)
    status.run()


if __name__ == "__main__":  # pragma: no cover
    main()
