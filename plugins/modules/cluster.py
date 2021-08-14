#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Gaelle Mangin (@gmangin)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: cluster
short_description: Create, update or delete clusters within Nautobot
description:
  - Creates, updates or removes clusters from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Gaelle MANGIN (@gmangin)
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
  name:
    description:
      - The name of the cluster
    required: true
    type: str
  cluster_type:
    description:
      - type of the cluster
    required: false
    type: raw
  cluster_group:
    description:
      - group of the cluster
    required: false
    type: raw
  site:
    description:
      - Required if I(state=present) and the cluster does not exist yet
    required: false
    type: raw
  comments:
    description:
      - Comments that may include additional information in regards to the cluster
    required: false
    type: str
  tenant:
    description:
      - Tenant the cluster will be assigned to.
    required: false
    type: raw
  tags:
    description:
      - Any tags that the cluster may need to be associated with
    required: false
    type: list
    elements: raw
  custom_fields:
    description:
      - must exist in Nautobot
    required: false
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
    - name: Create cluster within Nautobot with only required information
      networktocode.nautobot.cluster:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Cluster
        cluster_type: libvirt
        state: present

    - name: Delete cluster within nautobot
      networktocode.nautobot.cluster:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Cluster
        state: absent

    - name: Create cluster with tags
      networktocode.nautobot.cluster:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Another Test Cluster
        cluster_type: libvirt
        tags:
          - Schnozzberry
        state: present

    - name: Update the group and site of an existing cluster
      networktocode.nautobot.cluster:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Cluster
        cluster_type: qemu
        cluster_group: GROUP
        site: SITE
        state: present
"""

RETURN = r"""
cluster:
  description: Serialized object as created or already existent within Nautobot
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NAUTOBOT_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.virtualization import (
    NautobotVirtualizationModule,
    NB_CLUSTERS,
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
            name=dict(required=True, type="str"),
            cluster_type=dict(required=False, type="raw"),
            cluster_group=dict(required=False, type="raw"),
            site=dict(required=False, type="raw"),
            tenant=dict(required=False, type="raw"),
            comments=dict(required=False, type="str"),
            tags=dict(required=False, type="list", elements="raw"),
            custom_fields=dict(required=False, type="dict"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    cluster = NautobotVirtualizationModule(module, NB_CLUSTERS)
    cluster.run()


if __name__ == "__main__":  # pragma: no cover
    main()
