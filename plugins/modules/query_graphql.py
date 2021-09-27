#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""Ansible plugin definition for query_graphql action plugin."""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

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
            - Dictionary of keys/values to pass into the GraphQL query, see [pynautobot GraphQL documentation](https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html) for more details
        required: False
        type: dict
    query:
        description:
            - The GraphQL formatted query string, see [pynautobot GraphQL documentation](https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html) for more details.
        required: True
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
          sites {
            id
            name
            region {
              name
            }
          }
        }

  # Make query to GraphQL Endpoint
  - name: Obtain list of sites from Nautobot
    networktocode.nautobot.query_graphql:
      url: http://nautobot.local
      token: thisIsMyToken
      query: "{{ query_string }}"


  # Example with variables
  - name: SET FACTS TO SEND TO GRAPHQL ENDPOINT
    set_fact:
      variables:
        site_name: den
      query_string: |
        query ($site_name:String!) {
          sites (name: $site_name) {
            id
            name
            region {
                name
            }
          }
        }

  # Get Response with variables and set to root keys
  - name: Obtain list of devices at site in variables from Nautobot
    networktocode.nautobot.query_graphql:
      url: http://nautobot.local
      token: thisIsMyToken
      query: "{{ query_string }}"
      variables: "{{ variables }}"
      update_hostvars: "yes"
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
    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(changed=False, original_message="", message="")

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=dict(
            graph_variables=dict(required=False, type="dict", default={}),
            query=dict(required=True, type="str"),
            token=dict(required=False, type="str", no_log=True, default=None),
            url=dict(required=False, type="str", default=None),
            validate_certs=dict(required=False, type="bool", default=True),
            update_hostvars=dict(required=False, type="bool", default=False),
        ),
        # Set to true as this is a read only API, this may need to change or have significant changes when Mutations are
        # added to the GraphQL endpoint of Nautobot
        supports_check_mode=True,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
