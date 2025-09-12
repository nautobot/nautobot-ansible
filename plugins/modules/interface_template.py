#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: interface_template
short_description: Creates or removes interface templates from Nautobot
description:
  - Creates or removes interface templates from Nautobot
notes:
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network To Code (@networktocode)
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
  - networktocode.nautobot.fragments.custom_fields
options:
  id:
    required: false
    type: str
  name:
    required: true
    type: str
  label:
    required: false
    type: str
  description:
    required: false
    type: str
  type:
    required: true
    type: str
    choices:
      - "virtual"
      - "bridge"
      - "lag"
      - "100base-fx"
      - "100base-lfx"
      - "100base-tx"
      - "100base-t1"
      - "1000base-t"
      - "2.5gbase-t"
      - "5gbase-t"
      - "10gbase-t"
      - "10gbase-cx4"
      - "1000base-x-gbic"
      - "1000base-x-sfp"
      - "10gbase-x-sfpp"
      - "10gbase-x-xfp"
      - "10gbase-x-xenpak"
      - "10gbase-x-x2"
      - "25gbase-x-sfp28"
      - "50gbase-x-sfp56"
      - "40gbase-x-qsfpp"
      - "50gbase-x-sfp28"
      - "100gbase-x-cfp"
      - "100gbase-x-cfp2"
      - "200gbase-x-cfp2"
      - "400gbase-x-cfp2"
      - "100gbase-x-cfp4"
      - "100gbase-x-cpak"
      - "100gbase-x-qsfp28"
      - "100gbase-x-cxp"
      - "100gbase-x-qsfpdd"
      - "100gbase-x-dsfp"
      - "100gbase-x-sfpdd"
      - "200gbase-x-qsfp56"
      - "200gbase-x-qsfpdd"
      - "400gbase-x-qsfp112"
      - "400gbase-x-qsfpdd"
      - "400gbase-x-osfp"
      - "400gbase-x-osfp-rhs"
      - "400gbase-x-cdfp"
      - "400gbase-x-cfp8"
      - "800gbase-x-qsfpdd"
      - "800gbase-x-osfp"
      - "800gbase-x-osfp-xd"
      - "1600gbase-x-osfp"
      - "1600gbase-x-osfp-xd"
      - "1000base-kx"
      - "10gbase-kr"
      - "10gbase-kx4"
      - "25gbase-kr"
      - "40gbase-kr4"
      - "50gbase-kr"
      - "100gbase-kp4"
      - "100gbase-kr2"
      - "100gbase-kr4"
      - "ieee802.11a"
      - "ieee802.11g"
      - "ieee802.11n"
      - "ieee802.11ac"
      - "ieee802.11ad"
      - "ieee802.11ax"
      - "ieee802.11ay"
      - "ieee802.15.1"
      - "other-wireless"
      - "gsm"
      - "cdma"
      - "lte"
      - "sonet-oc3"
      - "sonet-oc12"
      - "sonet-oc48"
      - "sonet-oc192"
      - "sonet-oc768"
      - "sonet-oc1920"
      - "sonet-oc3840"
      - "1gfc-sfp"
      - "2gfc-sfp"
      - "4gfc-sfp"
      - "8gfc-sfpp"
      - "16gfc-sfpp"
      - "32gfc-sfp28"
      - "32gfc-sfpp"
      - "64gfc-qsfpp"
      - "64gfc-sfpdd"
      - "64gfc-sfpp"
      - "128gfc-sfp28"
      - "infiniband-sdr"
      - "infiniband-ddr"
      - "infiniband-qdr"
      - "infiniband-fdr10"
      - "infiniband-fdr"
      - "infiniband-edr"
      - "infiniband-hdr"
      - "infiniband-ndr"
      - "infiniband-xdr"
      - "t1"
      - "e1"
      - "t3"
      - "e3"
      - "da15"
      - "da26"
      - "da31"
      - "db25"
      - "db44"
      - "db60"
      - "dc37"
      - "dc62"
      - "dc79"
      - "dd50"
      - "dd78"
      - "dd100"
      - "de9"
      - "de15"
      - "de19"
      - "df104"
      - "xdsl"
      - "docsis"
      - "gpon"
      - "xg-pon"
      - "xgs-pon"
      - "ng-pon2"
      - "epon"
      - "10g-epon"
      - "cisco-stackwise"
      - "cisco-stackwise-plus"
      - "cisco-flexstack"
      - "cisco-flexstack-plus"
      - "cisco-stackwise-80"
      - "cisco-stackwise-160"
      - "cisco-stackwise-320"
      - "cisco-stackwise-480"
      - "cisco-stackwise-1t"
      - "juniper-vcp"
      - "extreme-summitstack"
      - "extreme-summitstack-128"
      - "extreme-summitstack-256"
      - "extreme-summitstack-512"
      - "other"
  mgmt_only:
    required: false
    type: bool
  device_type:
    required: false
    type: dict
  module_type:
    required: false
    type: dict
"""

EXAMPLES = r"""
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create interface_template within Nautobot with only required information
      networktocode.nautobot.interface_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Interface_Template
        type: virtual
        state: present

    - name: Delete interface_template within nautobot
      networktocode.nautobot.interface_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Interface_Template
        state: absent
"""

RETURN = r"""
interface_template:
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
from ansible_collections.networktocode.nautobot.plugins.module_utils.dcim import (
    NautobotDcimModule,
    NB_INTERFACE_TEMPLATES,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(deepcopy(CUSTOM_FIELDS_ARG_SPEC))
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            label=dict(required=False, type="str"),
            description=dict(required=False, type="str"),
            type=dict(
                required=True,
                type="str",
                choices=[
                    "virtual",
                    "bridge",
                    "lag",
                    "100base-fx",
                    "100base-lfx",
                    "100base-tx",
                    "100base-t1",
                    "1000base-t",
                    "2.5gbase-t",
                    "5gbase-t",
                    "10gbase-t",
                    "10gbase-cx4",
                    "1000base-x-gbic",
                    "1000base-x-sfp",
                    "10gbase-x-sfpp",
                    "10gbase-x-xfp",
                    "10gbase-x-xenpak",
                    "10gbase-x-x2",
                    "25gbase-x-sfp28",
                    "50gbase-x-sfp56",
                    "40gbase-x-qsfpp",
                    "50gbase-x-sfp28",
                    "100gbase-x-cfp",
                    "100gbase-x-cfp2",
                    "200gbase-x-cfp2",
                    "400gbase-x-cfp2",
                    "100gbase-x-cfp4",
                    "100gbase-x-cpak",
                    "100gbase-x-qsfp28",
                    "100gbase-x-cxp",
                    "100gbase-x-qsfpdd",
                    "100gbase-x-dsfp",
                    "100gbase-x-sfpdd",
                    "200gbase-x-qsfp56",
                    "200gbase-x-qsfpdd",
                    "400gbase-x-qsfp112",
                    "400gbase-x-qsfpdd",
                    "400gbase-x-osfp",
                    "400gbase-x-osfp-rhs",
                    "400gbase-x-cdfp",
                    "400gbase-x-cfp8",
                    "800gbase-x-qsfpdd",
                    "800gbase-x-osfp",
                    "800gbase-x-osfp-xd",
                    "1600gbase-x-osfp",
                    "1600gbase-x-osfp-xd",
                    "1000base-kx",
                    "10gbase-kr",
                    "10gbase-kx4",
                    "25gbase-kr",
                    "40gbase-kr4",
                    "50gbase-kr",
                    "100gbase-kp4",
                    "100gbase-kr2",
                    "100gbase-kr4",
                    "ieee802.11a",
                    "ieee802.11g",
                    "ieee802.11n",
                    "ieee802.11ac",
                    "ieee802.11ad",
                    "ieee802.11ax",
                    "ieee802.11ay",
                    "ieee802.15.1",
                    "other-wireless",
                    "gsm",
                    "cdma",
                    "lte",
                    "sonet-oc3",
                    "sonet-oc12",
                    "sonet-oc48",
                    "sonet-oc192",
                    "sonet-oc768",
                    "sonet-oc1920",
                    "sonet-oc3840",
                    "1gfc-sfp",
                    "2gfc-sfp",
                    "4gfc-sfp",
                    "8gfc-sfpp",
                    "16gfc-sfpp",
                    "32gfc-sfp28",
                    "32gfc-sfpp",
                    "64gfc-qsfpp",
                    "64gfc-sfpdd",
                    "64gfc-sfpp",
                    "128gfc-sfp28",
                    "infiniband-sdr",
                    "infiniband-ddr",
                    "infiniband-qdr",
                    "infiniband-fdr10",
                    "infiniband-fdr",
                    "infiniband-edr",
                    "infiniband-hdr",
                    "infiniband-ndr",
                    "infiniband-xdr",
                    "t1",
                    "e1",
                    "t3",
                    "e3",
                    "da15",
                    "da26",
                    "da31",
                    "db25",
                    "db44",
                    "db60",
                    "dc37",
                    "dc62",
                    "dc79",
                    "dd50",
                    "dd78",
                    "dd100",
                    "de9",
                    "de15",
                    "de19",
                    "df104",
                    "xdsl",
                    "docsis",
                    "gpon",
                    "xg-pon",
                    "xgs-pon",
                    "ng-pon2",
                    "epon",
                    "10g-epon",
                    "cisco-stackwise",
                    "cisco-stackwise-plus",
                    "cisco-flexstack",
                    "cisco-flexstack-plus",
                    "cisco-stackwise-80",
                    "cisco-stackwise-160",
                    "cisco-stackwise-320",
                    "cisco-stackwise-480",
                    "cisco-stackwise-1t",
                    "juniper-vcp",
                    "extreme-summitstack",
                    "extreme-summitstack-128",
                    "extreme-summitstack-256",
                    "extreme-summitstack-512",
                    "other",
                ],
            ),
            mgmt_only=dict(required=False, type="bool"),
            device_type=dict(required=False, type="dict"),
            module_type=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    interface_template = NautobotDcimModule(module, NB_INTERFACE_TEMPLATES)
    interface_template.run()


if __name__ == "__main__":  # pragma: no cover
    main()
