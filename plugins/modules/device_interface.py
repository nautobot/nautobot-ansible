#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: device_interface
short_description: Creates or removes interfaces on devices from Nautobot
description:
  - Creates or removes interfaces from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  device:
    description:
      - Name of the device the interface will be associated with (case-sensitive)
    required: true
    type: raw
    version_added: "3.0.0"
  status:
    description:
      - The status of the interface
      - Required if I(state=present) and using I(api_version) 1.4+
    required: false
    type: raw
    version_added: "4.5.0"
  name:
    description:
      - Name of the interface to be created
    required: true
    type: str
    version_added: "3.0.0"
  label:
    description:
      - Physical label of the interface
    required: false
    type: str
    version_added: "3.0.0"
  type:
    description:
      - |
        Form factor of the interface:
        ex. 1000Base-T (1GE), Virtual, 10GBASE-T (10GE)
        This has to be specified exactly as what is found within UI
    required: false
    type: str
    version_added: "3.0.0"
  enabled:
    description:
      - Sets whether interface shows enabled or disabled
    required: false
    type: bool
    version_added: "3.0.0"
  lag:
    description:
      - Parent LAG interface will be a member of
    required: false
    type: raw
    version_added: "3.0.0"
  parent_interface:
    description:
      - Interface that will be the parent of the interface being created
    required: false
    type: raw
    version_added: "4.5.0"
  bridge:
    description:
      - Interface that will be the bridge of the interface being created
    required: false
    type: raw
    version_added: "4.5.0"
  mtu:
    description:
      - The MTU of the interface
    required: false
    type: int
    version_added: "3.0.0"
  mac_address:
    description:
      - The MAC address of the interface
    required: false
    type: str
    version_added: "3.0.0"
  mgmt_only:
    description:
      - This interface is used only for out-of-band management
    required: false
    type: bool
    version_added: "3.0.0"
  description:
    description:
      - The description of the interface
    required: false
    type: str
    version_added: "3.0.0"
  mode:
    description:
      - The mode of the interface
    required: false
    type: raw
    version_added: "3.0.0"
  untagged_vlan:
    description:
      - The untagged VLAN to be assigned to interface
    required: false
    type: raw
    version_added: "3.0.0"
  tagged_vlans:
    description:
      - A list of tagged VLANS to be assigned to interface. Mode must be set to either C(Tagged) or C(Tagged All)
    required: false
    type: raw
    version_added: "3.0.0"
  update_vc_child:
    type: bool
    default: False
    description:
      - |
        Use when master device is specified for C(device) and the specified interface exists on a child device
        and needs updated
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot interface module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create interface within Nautobot with only required information
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: GigabitEthernet1
        state: present
    - name: Delete interface within nautobot
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: GigabitEthernet1
        state: absent
    - name: Create LAG with several specified options
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: port-channel1
        type: Link Aggregation Group (LAG)
        mtu: 1600
        mgmt_only: false
        mode: Access
        state: present
    - name: Create interface and assign it to parent LAG
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: GigabitEthernet1
        enabled: false
        type: 1000Base-t (1GE)
        lag:
          name: port-channel1
        mtu: 1600
        mgmt_only: false
        mode: Access
        state: present
    - name: Create interface as a trunk port
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: GigabitEthernet25
        enabled: false
        type: 1000Base-t (1GE)
        untagged_vlan:
          name: Wireless
          site: Test Site
        tagged_vlans:
          - name: Data
            site: Test Site
          - name: VoIP
            site: Test Site
        mtu: 1600
        mgmt_only: true
        mode: Tagged
        state: present
    - name: Update interface on child device on virtual chassis
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: GigabitEthernet2/0/1
        enabled: false
        update_vc_child: True
    - name: |
        Create an interface and update custom_field data point,
        setting the value to True
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: GigabitEthernet1/1/1
        enabled: false
        custom_fields:
          monitored: True
    - name: Create child interface
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: GigabitEthernet1/1/1
        type: Virtual
        parent_interface:
          name: GigabitEthernet1/1
    - name: Create bridge interface
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: Bridge1
        bridge:
          name: GigabitEthernet1/1
"""

RETURN = r"""
interface:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_INTERFACES,
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
            update_vc_child=dict(type="bool", required=False, default=False),
            device=dict(required=True, type="raw"),
            status=dict(required=False, type="raw"),
            name=dict(required=True, type="str"),
            label=dict(required=False, type="str"),
            type=dict(required=False, type="str"),
            enabled=dict(required=False, type="bool"),
            lag=dict(required=False, type="raw"),
            parent_interface=dict(required=False, type="raw"),
            bridge=dict(required=False, type="raw"),
            mtu=dict(required=False, type="int"),
            mac_address=dict(required=False, type="str"),
            mgmt_only=dict(required=False, type="bool"),
            description=dict(required=False, type="str"),
            mode=dict(required=False, type="raw"),
            untagged_vlan=dict(required=False, type="raw"),
            tagged_vlans=dict(required=False, type="raw"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    device_interface = NautobotDcimModule(module, NB_INTERFACES, remove_keys=["update_vc_child"])
    device_interface.run()


if __name__ == "__main__":  # pragma: no cover
    main()
