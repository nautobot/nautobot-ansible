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
module: rack_group
short_description: Create, update or delete racks groups within Nautobot
description:
  - Creates, updates or removes racks groups from Nautobot
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
      - Defines the rack group configuration
    suboptions:
      description:
        description:
          - The description of the rack group
        required: false
        type: str
      name:
        description:
          - The name of the rack group
        required: true
        type: str
      slug:
        description:
          - The slugified version of the name or custom slug.
          - This is auto-generated following Nautobot rules if not provided
        required: false
        type: str
      site:
        description:
          - Required if I(state=present) and the rack does not exist yet
        required: false
        type: raw
      parent_rack_group:
        description:
          - The parent rack-group the rack group will be assigned to
        required: false
        type: raw
      region:
        description:
          - The region the rack group will be assigned to
        required: false
        type: raw
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
    - name: Create rack group within Nautobot with only required information
      networktocode.nautobot.rack_group:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test rack group
          site: Test Site
        state: present

    - name: Delete rack group within nautobot
      networktocode.nautobot.rack_group:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Rack group
          site: Test Site
        state: absent
"""

RETURN = r"""
rack_group:
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
    NB_RACK_GROUPS,
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
                    description=dict(required=False, type="str"),
                    site=dict(required=False, type="raw"),
                    region=dict(required=False, type="raw"),
                    parent_rack_group=dict(required=False, type="raw"),
                ),
            ),
        )
    )

    required_if = [("state", "present", ["name"]), ("state", "absent", ["name"])]

    module = NautobotAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    rack_group = NautobotDcimModule(module, NB_RACK_GROUPS)
    rack_group.run()


if __name__ == "__main__":  # pragma: no cover
    main()
