#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: front_port_template
short_description: Create, update or delete front port templates within Nautobot
description:
  - Creates, updates or removes front port templates from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Tobias Groß (@toerb)
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
    required: true
    description:
      - Defines the front port template configuration
    suboptions:
      device_type:
        description:
          - The device type the front port template is attached to
        required: true
        type: raw
      name:
        description:
          - The name of the front port template
        required: true
        type: str
      type:
        description:
          - The type of the front port template
        choices:
          - 8p8c
          - 8p6c
          - 8p4c
          - 8p2c
          - gg45
          - tera-4p
          - tera-2p
          - tera-1p
          - 110-punch
          - bnc
          - mrj21
          - st
          - sc
          - sc-apc
          - fc
          - lc
          - lc-apc
          - mtrj
          - mpo
          - lsh
          - lsh-apc
          - splice
          - cs
          - sn
        required: false
        type: str
      rear_port_template:
        description:
          - The rear_port_template the front port template is attached to
        required: true
        type: raw        
      rear_port_template_position:
        description:
          - The position of the rear port template this front port template is connected to
        required: false
        type: int
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
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create front port template within Nautobot with only required information
      networktocode.nautobot.front_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Front Port Template
          device_type: Test Device Type
          type: bnc
          rear_port_template: Test Rear Port Template
        state: present

    - name: Update front port template with other fields
      networktocode.nautobot.front_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Front Port Template
          device_type: Test Device Type
          type: bnc
          rear_port_template: Test Rear Port Template
          rear_port_template_position: 5
        state: present

    - name: Delete front port template within nautobot
      networktocode.nautobot.front_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Front Port Template
          device_type: Test Device Type
          type: bnc
          rear_port_template: Test Rear Port Template
        state: absent
"""

RETURN = r"""
front_port_template:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_FRONT_PORT_TEMPLATES,
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
                    device_type=dict(required=True, type="raw"),
                    name=dict(required=True, type="str"),
                    type=dict(
                        required=False,
                        choices=[
                            "8p8c",
                            "8p6c",
                            "8p4c",
                            "8p2c",
                            "gg45",
                            "tera-4p",
                            "tera-2p",
                            "tera-1p",
                            "110-punch",
                            "bnc",
                            "mrj21",
                            "st",
                            "sc",
                            "sc-apc",
                            "fc",
                            "lc",
                            "lc-apc",
                            "mtrj",
                            "mpo",
                            "lsh",
                            "lsh-apc",
                            "splice",
                            "cs",
                            "sn",
                        ],
                        type="str",
                    ),
                    rear_port_template=dict(required=True, type="raw"),
                    rear_port_template_position=dict(required=False, type="int"),
                ),
            ),
        )
    )

    required_if = [
        ("state", "present", ["device_type", "name", "type", "rear_port_template"]),
        ("state", "absent", ["device_type", "name", "type", "rear_port_template"]),
    ]

    module = NautobotAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    front_port_template = NautobotDcimModule(module, NB_FRONT_PORT_TEMPLATES)
    front_port_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
