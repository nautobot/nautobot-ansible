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
module: device_role
short_description: Create, update or delete devices roles within Nautobot
description:
  - Creates, updates or removes devices roles from Nautobot
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
    description:
      - (deprecated) In the next version of the modules the `data` option will be removed. All sub options will now be an option of the module.
      - Defines the device role configuration
    suboptions:
      name:
        description:
          - The name of the device role
        required: true
        type: str
      description:
        description:
          - The description of the device role
        required: false
        type: str
      color:
        description:
          - Hexidecimal code for a color, ex. FFFFFF
        required: false
        type: str
      slug:
        description:
          - The slugified version of the name or custom slug.
          - This is auto-generated following Nautobot rules if not provided
        required: false
        type: str
      vm_role:
        description:
          - Whether the role is a VM role
        type: bool
    required: true
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
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create device role within Nautobot with only required information
      networktocode.nautobot.device_role:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test device role
          color: FFFFFF
        state: present

    - name: Delete device role within nautobot
      networktocode.nautobot.device_role:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Rack role
        state: absent
"""

RETURN = r"""
device_role:
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
    NB_DEVICE_ROLES,
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
                    description=dict(required=False, type="str"),
                    color=dict(required=False, type="str"),
                    slug=dict(required=False, type="str"),
                    vm_role=dict(required=False, type="bool"),
                ),
            ),
        )
    )

    required_if = [("state", "present", ["name"]), ("state", "absent", ["name"])]

    module = NautobotAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    device_role = NautobotDcimModule(module, NB_DEVICE_ROLES)
    device_role.run()


if __name__ == "__main__":  # pragma: no cover
    main()
