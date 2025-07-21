#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Gaelle Mangin (@gmangin)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: virtual_machine
short_description: Create, update or delete virtual_machines within Nautobot
description:
  - Creates, updates or removes virtual_machines from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Gaelle MANGIN (@gmangin)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.id
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  name:
    description:
      - The name of the virtual machine
      - Required if I(state=present) and the virtual machine does not exist yet
    required: false
    type: str
    version_added: "3.0.0"
  cluster:
    description:
      - The name of the cluster attach to the virtual machine
    required: false
    type: raw
    version_added: "3.0.0"
  role:
    description:
      - The role of the virtual machine
    required: false
    type: raw
    version_added: "3.0.0"
  vcpus:
    description:
      - Number of vcpus of the virtual machine
    required: false
    type: int
    version_added: "3.0.0"
  tenant:
    description:
      - The tenant that the virtual machine will be assigned to
    required: false
    type: raw
    version_added: "3.0.0"
  platform:
    description:
      - The platform of the virtual machine
    required: false
    type: raw
    version_added: "3.0.0"
  primary_ip4:
    description:
      - Primary IPv4 address assigned to the virtual machine
    required: false
    type: raw
    version_added: "3.0.0"
  primary_ip6:
    description:
      - Primary IPv6 address assigned to the virtual machine
    required: false
    type: raw
    version_added: "3.0.0"
  memory:
    description:
      - Memory of the virtual machine (MB)
    required: false
    type: int
    version_added: "3.0.0"
  disk:
    description:
      - Disk of the virtual machine (GB)
    required: false
    type: int
    version_added: "3.0.0"
  status:
    description:
      - The status of the virtual machine
      - Required if I(state=present) and does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  local_config_context_data:
    description:
      - configuration context of the virtual machine
    required: false
    type: dict
    version_added: "3.0.0"
  comments:
    description:
      - Comments of the virtual machine
    required: false
    type: str
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Create virtual machine within Nautobot with only required information
      networktocode.nautobot.virtual_machine:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Virtual Machine
        cluster: test cluster
        status: active
        state: present

    - name: Delete virtual machine within nautobot
      networktocode.nautobot.virtual_machine:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Virtual Machine
        state: absent

    - name: Create virtual machine with tags
      networktocode.nautobot.virtual_machine:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Another Test Virtual Machine
        cluster: test cluster
        status: active
        tags:
          - Schnozzberry
        state: present

    - name: Update vcpus, memory and disk of an existing virtual machine
      networktocode.nautobot.virtual_machine:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Virtual Machine
        cluster: test cluster
        vcpus: 8
        memory: 8
        disk: 8
        state: present

    - name: Delete virtual machine by id
      networktocode.nautobot.virtual_machine:
        url: http://nautobot.local
        token: thisIsMyToken
        id: 00000000-0000-0000-0000-000000000000
        state: absent
"""

RETURN = r"""
virtual machine:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    CUSTOM_FIELDS_ARG_SPEC,
    ID_ARG_SPEC,
    NAUTOBOT_ARG_SPEC,
    TAGS_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.virtualization import (
    NB_VIRTUAL_MACHINES,
    NautobotVirtualizationModule,
)


def main():
    """
    Main entry point for module execution.
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(ID_ARG_SPEC))
    argument_spec.update(deepcopy(TAGS_ARG_SPEC))
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=False, type="str"),
            cluster=dict(required=False, type="raw"),
            role=dict(required=False, type="raw"),
            vcpus=dict(required=False, type="int"),
            tenant=dict(required=False, type="raw"),
            platform=dict(required=False, type="raw"),
            primary_ip4=dict(required=False, type="raw"),
            primary_ip6=dict(required=False, type="raw"),
            memory=dict(required=False, type="int"),
            disk=dict(required=False, type="int"),
            status=dict(required=False, type="raw"),
            local_config_context_data=dict(required=False, type="dict"),
            comments=dict(required=False, type="str"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    virtual_machine = NautobotVirtualizationModule(module, NB_VIRTUAL_MACHINES)
    virtual_machine.run()


if __name__ == "__main__":  # pragma: no cover
    main()
