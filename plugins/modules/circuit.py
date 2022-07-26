#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: circuit
short_description: Create, update or delete circuits within Nautobot
description:
  - Creates, updates or removes circuits from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
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
  cid:
    description:
      - The circuit id of the circuit
    required: true
    type: str
    version_added: "3.0.0"
  provider:
    description:
      - The provider of the circuit
    required: false
    type: raw
    version_added: "3.0.0"
  circuit_type:
    description:
      - The circuit type of the circuit
    required: false
    type: raw
    version_added: "3.0.0"
  status:
    description:
      - The status of the circuit
      - Required if I(state=present) and does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  tenant:
    description:
      - The tenant assigned to the circuit
    required: false
    type: raw
    version_added: "3.0.0"
  install_date:
    description:
      - The date the circuit was installed. e.g. YYYY-MM-DD
    required: false
    type: str
    version_added: "3.0.0"
  commit_rate:
    description:
      - Commit rate of the circuit (Kbps)
    required: false
    type: int
    version_added: "3.0.0"
  description:
    description:
      - Description of the circuit
    required: false
    type: str
    version_added: "3.0.0"
  comments:
    description:
      - Comments related to circuit
    required: false
    type: str
    version_added: "3.0.0"
  tags:
    description:
      - Any tags that the device may need to be associated with
    required: false
    type: list
    elements: raw
    version_added: "3.0.0"
  custom_fields:
    description:
      - must exist in Nautobot
    required: false
    type: dict
    version_added: "3.0.0"
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
    - name: Create circuit within Nautobot with only required information
      networktocode.nautobot.circuit:
        url: http://nautobot.local
        token: thisIsMyToken
        cid: Test Circuit
        provider: Test Provider
        circuit_type: Test Circuit Type
        status: active
        state: present

    - name: Update circuit with other fields
      networktocode.nautobot.circuit:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
        cid: Test-Circuit-1000
        provider: Test Provider
        circuit_type: Test Circuit Type
        status: Active
        tenant: Test Tenant
        install_date: "2018-12-25"
        commit_rate: 10000
        description: Test circuit
        comments: "FAST CIRCUIT"
        state: present

    - name: Delete circuit within nautobot
      networktocode.nautobot.circuit:
        url: http://nautobot.local
        token: thisIsMyToken
        cid: Test-Circuit-1000
        state: absent
"""

RETURN = r"""
circuit:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.circuits import (
    NautobotCircuitsModule,
    NB_CIRCUITS,
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
            cid=dict(required=True, type="str"),
            provider=dict(required=False, type="raw"),
            circuit_type=dict(required=False, type="raw"),
            status=dict(required=False, type="raw"),
            tenant=dict(required=False, type="raw"),
            install_date=dict(required=False, type="str"),
            commit_rate=dict(required=False, type="int"),
            description=dict(required=False, type="str"),
            comments=dict(required=False, type="str"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
        )
    )

    required_if = [
        ("state", "present", ["cid", "status"]),
        ("state", "absent", ["cid"]),
    ]

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=required_if)

    circuit = NautobotCircuitsModule(module, NB_CIRCUITS)
    circuit.run()


if __name__ == "__main__":  # pragma: no cover
    main()
