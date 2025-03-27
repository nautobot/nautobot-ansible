# -*- coding: utf-8 -*-
# Copyright: (c) 2020, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
A lookup function designed to return data from the Nautobot GraphQL endpoint
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: lookup_graphql
    author: Josh VanDeraa (@jvanderaa)
    version_added: "1.1.0"
    short_description: Queries and returns elements from Nautobot GraphQL endpoint
    description:
        - Queries Nautobot via its GraphQL API through pynautobot
    options:
        api_version:
            description:
                - The Nautobot Rest API Version to use
            required: False
            version_added: "4.1.0"
        query:
            description:
                - The GraphQL formatted query string, see [pynautobot GraphQL documentation](https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html).
            required: True
        token:
            description:
                - The API token created through Nautobot
            env:
                # in order of precedence
                - name: NAUTOBOT_TOKEN
            required: False
        url:
            description:
                - The URL to the Nautobot instance to query (http://nautobot.example.com:8000)
            env:
                # in order of precedence
                - name: NAUTOBOT_URL
            required: True
        validate_certs:
            description:
                - Whether or not to validate SSL of the Nautobot instance
            required: False
            default: True
        graph_variables:
            description:
                - Dictionary of keys/values to pass into the GraphQL query
                - See [pynautobot GraphQL documentation](https://pynautobot.readthedocs.io/en/latest/advanced/graphql.html) for more details
            required: False
    requirements:
        - pynautobot
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
  set_fact:
    query_response: "{{ query('networktocode.nautobot.lookup_graphql', query=query_string, url='https://nautobot.example.com', token='<redact>') }}"

# Example with variables
- name: SET FACTS TO SEND TO GRAPHQL ENDPOINT
  set_fact:
    graph_variables:
      location_name: DEN
    query_string: |
      query ($location_name:[String]) {
        locations (name: $location_name) {
          id
          name
          parent {
            name
          }
        }
      }

# Get Response with variables
- name: Obtain list of devices from Nautobot
  set_fact:
    query_response: "{{ query('networktocode.nautobot.lookup_graphql', query_string, graph_variables=graph_variables,
    url='https://nautobot.example.com', token='<redact>') }}"
"""

RETURN = """
  data:
    description:
      - Data result from the GraphQL endpoint
    type: dict
"""

import os

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleLookupError, AnsibleError
from ansible.module_utils.six import raise_from

try:
    import pynautobot
except ImportError as imp_exc:
    PYNAUTOBOT_IMPORT_ERROR = imp_exc
else:
    PYNAUTOBOT_IMPORT_ERROR = None

try:
    from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
        NautobotApiBase,
        NautobotGraphQL,
        is_truthy,
    )
except ModuleNotFoundError:
    # For testing
    from plugins.module_utils.utils import NautobotApiBase, NautobotGraphQL

from ansible.utils.display import Display


def nautobot_lookup_graphql(**kwargs):
    """Lookup functionality, broken out to assist with testing

    Returns:
        [type]: [description]
    """
    # Add in logic on query to unpack
    query = kwargs.get("query")
    Display().v("Query String: %s" % query)

    # Check that a valid query was passed in
    if query is None:
        raise AnsibleLookupError("Query parameter was not passed. Please verify that query is passed.")
    # Setup API Token information, URL, and SSL verification
    url = kwargs.get("url") or os.getenv("NAUTOBOT_URL")
    Display().v("Nautobot URL: %s" % url)

    # Verify URL is passed in, that it is not None
    if url is None:
        raise AnsibleLookupError("Missing URL of Nautobot")

    token = kwargs.get("token") or os.getenv("NAUTOBOT_TOKEN")

    if kwargs.get("validate_certs") is not None:
        ssl_verify = kwargs.get("validate_certs")
    elif os.getenv("NAUTOBOT_VALIDATE_CERTS") is not None:
        ssl_verify = is_truthy(os.getenv("NAUTOBOT_VALIDATE_CERTS"))
    else:
        ssl_verify = True

    api_version = kwargs.get("api_version")
    Display().vv("Validate certs: %s" % ssl_verify)

    if not isinstance(ssl_verify, bool):
        raise AnsibleLookupError("validate_certs must be a boolean")

    nautobot_api = NautobotApiBase(token=token, url=url, ssl_verify=ssl_verify, api_version=api_version)
    graph_variables = kwargs.get("graph_variables")
    Display().v("Graph Variables: %s" % graph_variables)

    # Verify that the query is a string type
    if not isinstance(query, str):
        raise AnsibleLookupError("Query parameter must be of type string. Please see docs for examples.")

    # Verify that the variables key coming in is a dictionary
    if graph_variables is not None and not isinstance(graph_variables, dict):
        raise AnsibleLookupError("graph_variables parameter must be of key/value pairs. Please see docs for examples.")

    # Setup return results
    results = {}
    # Make call to Nautobot API and capture any failures
    nautobot_graph_obj = NautobotGraphQL(query_str=query, api=nautobot_api, variables=graph_variables)

    # Get the response from the object
    nautobot_response = nautobot_graph_obj.query()

    # Check for errors in the response
    if isinstance(nautobot_response, pynautobot.core.graphql.GraphQLException):
        raise AnsibleLookupError("Error in the query to the Nautobot host. Errors: %s" % (nautobot_response.errors))

    # Good result, return it
    if isinstance(nautobot_response, pynautobot.core.graphql.GraphQLRecord):
        # Assign the data of a good result to the response
        results = nautobot_response.json

    return [results]


class LookupModule(LookupBase):
    """
    LookupModule(LookupBase) is defined by Ansible
    """

    def run(self, terms, variables=None, graph_variables=None, **kwargs):
        """Runs Ansible Lookup Plugin for using Nautobot GraphQL endpoint

        Raises:
            AnsibleLookupError: Error in data loaded into the plugin

        Returns:
            dict: Data returned from GraphQL endpoint
        """
        if PYNAUTOBOT_IMPORT_ERROR:
            raise_from(
                AnsibleError("pynautobot must be installed to use this plugin"),
                PYNAUTOBOT_IMPORT_ERROR,
            )

        # Terms comes in as a list, this needs to be moved to string for pynautobot
        lookup_info = nautobot_lookup_graphql(query=terms[0], variables=variables, graph_variables=graph_variables, **kwargs)

        # Results should be the data response of the query to be returned as a lookup
        return lookup_info
