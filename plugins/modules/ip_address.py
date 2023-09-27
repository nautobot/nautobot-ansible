#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ip_address
short_description: Creates or removes IP addresses from Nautobot
description:
  - Creates or removes IP addresses from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
  - Anthony Ruhier (@Anthony25)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.tags
  - networktocode.nautobot.fragments.custom_fields
options:
  address:
    description:
      - Required if state is C(present)
    required: false
    type: str
    version_added: "3.0.0"
  namespace:
    description:
      - |
        namespace that IP address is associated with. IPs are unique per namespaces.
    required: false
    default: Global
    type: str
    version_added: "5.0.0"
  parent:
    description:
      - |
        With state C(new), it will force to get the next available IP in
        this prefix.
        Required if state is C(present) or C(new) when no address is given.
        Unused if an address is specified.
    required: false
    type: raw
    version_added: "3.0.0"
  tenant:
    description:
      - The tenant that the device will be assigned to
    required: false
    type: raw
    version_added: "3.0.0"
  status:
    description:
      - The status of the IP address
      - Required if I(state=present) and does not exist yet
    required: false
    type: raw
    version_added: "3.0.0"
  role:
    description:
      - The role of the IP address
    choices:
      - Loopback
      - Secondary
      - Anycast
      - VIP
      - VRRP
      - HSRP
      - GLBP
      - CARP
    required: false
    type: str
    version_added: "3.0.0"
  type:
    description:
      - The type of the IP address
    choices:
      - DHCP
      - Host
      - SLAAC
    required: false
    type: str
    version_added: "5.0.0"
  description:
    description:
      - The description of the interface
    required: false
    type: str
    version_added: "3.0.0"
  nat_inside:
    description:
      - The inside IP address this IP is assigned to
    required: false
    type: raw
    version_added: "3.0.0"
  dns_name:
    description:
      - Hostname or FQDN
    required: false
    type: str
    version_added: "3.0.0"
  state:
    description:
      - |
        Use C(present), C(new) or C(absent) for adding, force adding or removing.
        C(present) will check if the IP is already created, and return it if
        true. C(new) will force to create it anyway (useful for anycasts, for
        example).
    choices: [ absent, new, present ]
    default: present
    type: str
"""

EXAMPLES = r"""
- name: "Test Nautobot IP address module"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create IP address within Nautobot with only required information
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: 192.168.1.10
        status: active
        state: present
    - name: Force to create (even if it already exists) the IP
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: 192.168.1.10
        state: new
    - name: Create the same IP under another namespace
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: 192.168.1.10
        namespace: MyNewNamespace
        state: new
    - name: Get a new available IP inside 192.168.1.0/24
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        parent: 192.168.1.0/24
        state: new
    - name: Delete IP address within nautobot
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: 192.168.1.10
        state: absent
    - name: Create IP address with several specified options in namespace Private
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: 192.168.1.20
        tenant: Test Tenant
        status: Reserved
        namespace: Private
        role: Loopback
        description: Test description
        tags:
          - Schnozzberry
        state: present
    - name: Create IP address and assign a nat_inside IP
      networktocode.nautobot.ip_address:
        url: http://nautobot.local
        token: thisIsMyToken
        address: 192.168.1.30
        nat_inside:
          address: 192.168.1.20
"""

RETURN = r"""
ip_address:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
    NautobotIpamModule,
    NB_IP_ADDRESSES,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    # state choices present, absent, new
    argument_spec["state"] = dict(required=False, default="present", choices=["present", "absent", "new"])
    argument_spec.update(
        dict(
            address=dict(required=False, type="str"),
            parent=dict(required=False, type="raw"),
            tenant=dict(required=False, type="raw"),
            status=dict(required=False, type="raw"),
            role=dict(
                required=False,
                type="str",
                choices=["Loopback", "Secondary", "Anycast", "VIP", "VRRP", "HSRP", "GLBP", "CARP"],
            ),
            type=dict(
                required=False,
                type="str",
                choices=["DHCP", "Host", "SLAAC"],
                default="Host",
            ),
            description=dict(required=False, type="str"),
            nat_inside=dict(required=False, type="raw"),
            dns_name=dict(required=False, type="str"),
            namespace=dict(required=False, type="str", default="Global"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
        )
    )

    required_if = [
        ("state", "present", ["address", "parent", "status"], True),
        ("state", "absent", ["address"]),
        ("state", "new", ["address", "parent"], True),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=required_if,
    )

    ip_address = NautobotIpamModule(module, NB_IP_ADDRESSES)
    ip_address.run()


if __name__ == "__main__":  # pragma: no cover
    main()
