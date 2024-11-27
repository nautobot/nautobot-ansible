#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2023, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: job_button
short_description: Creates or removes job buttons from Nautobot
description:
  - Creates or removes job buttons from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Travis Smith (@tsm1th)
requirements:
  - pynautobot
version_added: "5.4.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  name:
    description:
      - The name of the job button
    required: true
    type: str
  content_types:
    description:
      - The content types to associate the job button with
      - Required if I(state=present) and the job button does not exist yet
    required: false
    type: list
    element: str
  job:
    description:
      - The job receiver to associate job with
      - Required if I(state=present) and the job button does not exist yet
    required: false
    type: str
  enabled:
    description:
      - Whether or not the button is enabled
    required: false
    type: bool
  text:
    description:
      - The text to display on the button
      - Required if I(state=present) and the job button does not exist yet
    required: false
    type: str
  weight:
    description:
      - Position this field should be displayed in
    required: false
    type: int
  group_name:
    description:
      - Buttons in the same group will appear in a dropdown menu
    required: false
    type: str
  button_class:
    description:
      - Button class of this button
      - Required if I(state=present) and the job button does not exist yet
    required: false
    choices:
      - default
      - primary
      - success
      - info
      - warning
      - danger
      - link
    type: str
  confirmation:
    description:
      - Whether or not a confirmation pop-up box will appear
    required: false
    type: bool
"""

EXAMPLES = r"""
- name: Create job button within Nautobot with only required information
  networktocode.nautobot.job_button:
    url: http://nautobot.local
    token: thisIsMyToken
    name: MyJobButton
    content_types:
        - dcim.device
    job: MyJob
    text: SubmitMe
    state: present

- name: Delete job button within Nautobot
  networktocode.nautobot.job_button:
    url: http://nautobot.local
    token: thisIsMyToken
    name: MyJobButton
    state: absent
"""

RETURN = r"""
job_button:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.extras import (
    NautobotExtrasModule,
    NB_JOB_BUTTONS,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """Execute job button module."""
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            content_types=dict(required=False, type="list", elements="str"),
            job=dict(required=False, type="raw"),
            enabled=dict(required=False, type="bool"),
            text=dict(required=False, type="str"),
            weight=dict(required=False, type="int"),
            group_name=dict(required=False, type="str"),
            button_class=dict(required=False, choices=["default", "primary", "success", "info", "warning", "danger", "link"], type="str"),
            confirmation=dict(required=False, type="bool"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    job_button = NautobotExtrasModule(module, NB_JOB_BUTTONS)
    job_button.run()


if __name__ == "__main__":  # pragma: no cover
    main()
