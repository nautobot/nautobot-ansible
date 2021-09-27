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
module: rir
short_description: Create, update or delete RIRs within Nautobot
description:
  - Creates, updates or removes RIRs from Nautobot
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
    type: dict
    description:
      - (deprecated) In the next version of the modules the `data` option will be removed. All sub options will now be an option of the module.
      - Defines the RIR configuration
    suboptions:
      name:
        description:
          - The name of the RIR
        required: true
        type: str
      slug:
        description:
          - The slugified version of the name or custom slug.
          - This is auto-generated following Nautobot rules if not provided
        required: false
        type: str
      is_private:
        description:
          - IP space managed by this RIR is considered private
        required: false
        type: bool
    required: true
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
    - name: Create RIR within Nautobot with only required information
      networktocode.nautobot.rir:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test RIR One
        state: present

    - name: Update Test RIR One
      networktocode.nautobot.rir:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test RIR One
          is_private: True
        state: present

    - name: Delete RIR within nautobot
      networktocode.nautobot.rir:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test RIR One
        state: absent
"""

RETURN = r"""
rir:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
    NautobotIpamModule,
    NB_RIRS,
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
                    slug=dict(required=False, type="str"),
                    is_private=dict(required=False, type="bool"),
                ),
            ),
        )
    )

    required_if = [("state", "present", ["name"]), ("state", "absent", ["name"])]

    module = NautobotAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    rir = NautobotIpamModule(module, NB_RIRS)
    rir.run()


if __name__ == "__main__":  # pragma: no cover
    main()
