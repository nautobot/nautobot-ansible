#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: software_image_file
short_description: Creates or removes software image files from Nautobot
description:
  - Creates or removes software image files from Nautobot
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
  image_file_name:
    required: true
    type: str
  image_file_checksum:
    required: false
    type: str
  hashing_algorithm:
    required: false
    type: str
    choices:
      - "md5"
      - "sha1"
      - "sha224"
      - "sha384"
      - "sha256"
      - "sha512"
      - "sha3"
      - "blake2"
      - "blake3"
  image_file_size:
    required: false
    type: int
  download_url:
    required: false
    type: str
  default_image:
    required: false
    type: bool
  software_version:
    required: true
    type: dict
  external_integration:
    required: false
    type: dict
  status:
    required: true
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Create software_image_file within Nautobot with only required information
      networktocode.nautobot.software_image_file:
        url: http://nautobot.local
        token: thisIsMyToken
        image_file_name: "Test image_file_name"
        software_version: None
        status: "Active"
        state: present

    - name: Delete software_image_file within nautobot
      networktocode.nautobot.software_image_file:
        url: http://nautobot.local
        token: thisIsMyToken
        state: absent
"""

RETURN = r"""
software_image_file:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NB_SOFTWARE_IMAGE_FILES,
    NautobotDcimModule,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(
        dict(
            image_file_name=dict(required=True, type="str"),
            image_file_checksum=dict(required=False, type="str"),
            hashing_algorithm=dict(
                required=False,
                type="str",
                choices=[
                    "md5",
                    "sha1",
                    "sha224",
                    "sha384",
                    "sha256",
                    "sha512",
                    "sha3",
                    "blake2",
                    "blake3",
                ],
            ),
            image_file_size=dict(required=False, type="int"),
            download_url=dict(required=False, type="str"),
            default_image=dict(required=False, type="bool"),
            software_version=dict(required=True, type="dict"),
            external_integration=dict(required=False, type="dict"),
            status=dict(required=True, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    software_image_file = NautobotDcimModule(module, NB_SOFTWARE_IMAGE_FILES)
    software_image_file.run()


if __name__ == "__main__":  # pragma: no cover
    main()
