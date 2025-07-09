#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Ansible plugin definition for query_graphql action plugin."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: query_graphql
author: Josh VanDeraa (@jvanderaa)
version_added: "1.1.0"
short_description: Queries and returns elements from Nautobot GraphQL endpoint
description:
    - Queries Nautobot via its GraphQL API through pynautobot
requirements:
    - pynautobot
options:
    graph_variables:
        description:
            - Dictionary of keys/values to pass into the GraphQL query, see (U(https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html)) for more info
        required: False
        type: dict
        default: {}
    query:
        description:
            - The GraphQL formatted query string, see (U(https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html)) for more details.
        required: True
        type: str
    api_version:
        description:
          - API Version Nautobot REST API
        required: false
        type: str
    token:
        description:
            - The API token created through Nautobot, optional env=NAUTOBOT_TOKEN
        required: False
        type: str
    url:
        description:
            - The URL to the Nautobot instance to query (http://nautobot.example.com:8000), optional env=NAUTOBOT_URL
        required: False
        type: str
    validate_certs:
        description:
            - Whether or not to validate SSL of the Nautobot instance
        required: False
        default: True
        type: bool
    update_hostvars:
        description:
            - Whether or not to populate data in the in the root (e.g. hostvars[inventory_hostname]) or within the
              'data' key (e.g. hostvars[inventory_hostname]['data']). Beware, that the root keys provided by the query
              will overwrite any root keys already present, leverage the GraphQL alias feature to avoid issues.
        required: False
        default: False
        type: bool
"""

EXAMPLES = """
# Make API Query without variables
- name: SET FACT OF STRING
  set_fact:
    query_string: |
      query {
        locations {
          id
          name
          parent {
            name
          }
        }
      }

# Make query to GraphQL Endpoint
- name: Obtain list of locations from Nautobot
  networktocode.nautobot.query_graphql:
    url: http://nautobot.local
    token: thisIsMyToken
    query: "{{ query_string }}"


# Example with variables
- name: SET FACTS TO SEND TO GRAPHQL ENDPOINT
  set_fact:
    graph_variables:
      location_name: AMS01
    query_string: |
      query (location_name: String!) {
        locations (name: location_name) {
          id
          name
          parent {
              name
          }
        }
      }

# Get Response with variables and set to root keys
- name: Obtain list of devices at location in variables from Nautobot
  networktocode.nautobot.query_graphql:
    url: http://nautobot.local
    token: thisIsMyToken
    query: "{{ query_string }}"
    graph_variables: "{{ graph_variables }}"
    update_hostvars: true
"""

RETURN = """
  data:
    description:
      - Data result from the GraphQL endpoint
    type: dict
    returned: success
  url:
    description:
      - Nautobot URL that was supplied for troubleshooting
    returned: success
    type: str
  query:
    description:
      - Query string that was sent to Nautobot
    returned: success
    type: str
  graph_variables:
    description:
      - Variables passed in
    returned: success
    type: dict
"""
from ansible.module_utils.basic import AnsibleModule


def main():
    """Main definition of Action Plugin for query_graphql."""
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    AnsibleModule(
        argument_spec=dict(
            graph_variables=dict(required=False, type="dict", default={}),
            query=dict(required=True, type="str"),
            token=dict(required=False, type="str", no_log=True, default=None),
            url=dict(required=False, type="str", default=None),
            api_version=dict(required=False, type="str", default=None),
            validate_certs=dict(required=False, type="bool", default=True),
            update_hostvars=dict(required=False, type="bool", default=False),
        ),
        # Set to true as this is a read only API, this may need to change or have significant changes when Mutations are
        # added to the GraphQL endpoint of Nautobot
        supports_check_mode=True,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
