#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: software_version
short_description: Creates or removes software versions from Nautobot
description:
  - Creates or removes software versions from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  version:
    required: true
    type: str
  alias:
    required: false
    type: str
  release_date:
    required: false
    type: str
  end_of_support_date:
    required: false
    type: str
  documentation_url:
    required: false
    type: str
  long_term_support:
    required: false
    type: bool
  pre_release:
    required: false
    type: bool
  platform:
    required: true
    type: dict
  status:
    required: true
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create software_version within Nautobot with only required information
      networktocode.nautobot.software_version:
        url: http://nautobot.local
        token: thisIsMyToken
        version: "Test version"
        platform: None
        status: "Active"
        state: present

    - name: Delete software_version within nautobot
      networktocode.nautobot.software_version:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
software_version:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import CUSTOM_FIELDS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import TAGS_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_SOFTWARE_VERSIONS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            version=dict(required=True, type="str"),
            alias=dict(required=False, type="str"),
            release_date=dict(required=False, type="str"),
            end_of_support_date=dict(required=False, type="str"),
            documentation_url=dict(required=False, type="str"),
            long_term_support=dict(required=False, type="bool"),
            pre_release=dict(required=False, type="bool"),
            platform=dict(required=True, type="dict"),
            status=dict(required=True, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    software_version = NautobotDcimModule(module, NB_SOFTWARE_VERSIONS)
    software_version.run()


if __name__ == "__main__":  # pragma: no cover
    main()
