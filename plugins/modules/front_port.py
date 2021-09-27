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
module: front_port
short_description: Create, update or delete front ports within Nautobot
description:
  - Creates, updates or removes front ports from Nautobot
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
      - (deprecated) In the next version of the modules the `data` option will be removed. All sub options will now be an option of the module.
      - Defines the front port configuration
    suboptions:
      device:
        description:
          - The device the front port is attached to
        required: true
        type: raw
      name:
        description:
          - The name of the front port
        required: true
        type: str
      type:
        description:
          - The type of the front port
        choices:
          - 8p8c
          - 110-punch
          - bnc
          - mrj21
          - fc
          - lc
          - lc-apc
          - lsh
          - lsh-apc
          - mpo
          - mtrj
          - sc
          - sc-apc
          - st
        required: true
        type: str
      rear_port:
        description:
          - The rear_port the front port is attached to
        required: true
        type: raw        
      rear_port_position:
        description:
          - The position of the rear port this front port is connected to
        required: false
        type: int
      description:
        description:
          - Description of the front port
        required: false
        type: str
      tags:
        description:
          - Any tags that the front port may need to be associated with
        required: false
        type: list
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
    - name: Create front port within Nautobot with only required information
      networktocode.nautobot.front_port:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Front Port
          device: Test Device
          type: bnc
          rear_port: Test Rear Port
        state: present

    - name: Update front port with other fields
      networktocode.nautobot.front_port:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Front Port
          device: Test Device
          type: bnc
          rear_port: Test Rear Port
          rear_port_position: 5
          description: front port description
        state: present

    - name: Delete front port within nautobot
      networktocode.nautobot.front_port:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Front Port
          device: Test Device
          type: bnc
          rear_port: Test Rear Port
        state: absent
"""

RETURN = r"""
front_port:
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
    NB_FRONT_PORTS,
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
                    device=dict(required=True, type="raw"),
                    name=dict(required=True, type="str"),
                    type=dict(
                        required=True,
                        choices=[
                            "8p8c",
                            "110-punch",
                            "bnc",
                            "mrj21",
                            "fc",
                            "lc",
                            "lc-apc",
                            "lsh",
                            "lsh-apc",
                            "mpo",
                            "mtrj",
                            "sc",
                            "sc-apc",
                            "st",
                        ],
                        type="str",
                    ),
                    rear_port=dict(required=True, type="raw"),
                    rear_port_position=dict(required=False, type="int"),
                    description=dict(required=False, type="str"),
                    tags=dict(required=False, type="list"),
                ),
            ),
        )
    )

    required_if = [
        ("state", "present", ["device", "name", "type", "rear_port"]),
        ("state", "absent", ["device", "name", "type", "rear_port"]),
    ]

    module = NautobotAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    front_port = NautobotDcimModule(module, NB_FRONT_PORTS)
    front_port.run()


if __name__ == "__main__":  # pragma: no cover
    main()
