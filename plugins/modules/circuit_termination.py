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
module: circuit_termination
short_description: Create, update or delete circuit terminations within Nautobot
description:
  - Creates, updates or removes circuit terminations from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network to Code (@networktocode)
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
    required: true
    type: dict
    description:
      - (deprecated) In the next version of the modules the `data` option will be removed. All sub options will now be an option of the module.
      - Defines the circuit termination configuration
    suboptions:
      circuit:
        description:
          - The circuit to assign to circuit termination
        required: true
        type: raw
      term_side:
        description:
          - The side of the circuit termination
        choices:
          - A
          - Z
        required: true
        type: str
      site:
        description:
          - The site the circuit termination will be assigned to
        required: false
        type: raw
      port_speed:
        description:
          - The speed of the port (Kbps)
        required: false
        type: int
      upstream_speed:
        description:
          - The upstream speed of the circuit termination
        required: false
        type: int
      xconnect_id:
        description:
          - The cross connect ID of the circuit termination
        required: false
        type: str
      pp_info:
        description:
          - Patch panel information
        required: false
        type: str
      description:
        description:
          - Description of the circuit termination
        required: false
        type: str
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
    - name: Create circuit termination within Nautobot with only required information
      networktocode.nautobot.circuit_termination:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          circuit: Test Circuit
          term_side: A
          site: Test Site
          port_speed: 10000
        state: present

    - name: Update circuit termination with other fields
      networktocode.nautobot.circuit_termination:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          circuit: Test Circuit
          term_side: A
          upstream_speed: 1000
          xconnect_id: 10X100
          pp_info: PP10-24
          description: "Test description"
        state: present

    - name: Delete circuit termination within nautobot
      networktocode.nautobot.circuit_termination:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          circuit: Test Circuit
          term_side: A
        state: absent
"""

RETURN = r"""
circuit_termination:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.circuits import (
    NautobotCircuitsModule,
    NB_CIRCUIT_TERMINATIONS,
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
                    circuit=dict(required=True, type="raw"),
                    term_side=dict(required=True, choices=["A", "Z"]),
                    site=dict(required=False, type="raw"),
                    port_speed=dict(required=False, type="int"),
                    upstream_speed=dict(required=False, type="int"),
                    xconnect_id=dict(required=False, type="str"),
                    pp_info=dict(required=False, type="str"),
                    description=dict(required=False, type="str"),
                ),
            ),
        )
    )

    required_if = [
        ("state", "present", ["circuit", "term_side"]),
        ("state", "absent", ["circuit", "term_side"]),
    ]

    module = NautobotAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    circuit_termination = NautobotCircuitsModule(module, NB_CIRCUIT_TERMINATIONS)
    circuit_termination.run()


if __name__ == "__main__":  # pragma: no cover
    main()
