"""GraphQL related filter plugins."""

# Copyright (c) 2022, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
name: graphql_string
author: Mikhail Yohman (@FragmentedPacket)
version_added: "3.4.0"
short_description: The graphql_string filter plugin.
description:
  - The filter converts a dictionary to a GraphQL string.
options:
  query:
    description:
      - A dictionary mapping to the GraphQL call to be made.
    type: dict
    required: True
  start:
    description:
      - The starting indentation when compiling the string.
    type: int
    required: False
"""

RETURN = r"""
graphql_string:
  description: GraphQL query string
  returned: always
  type: str
"""

EXAMPLES = r"""
# Code:
- set_fact:
    gql_query: "{{ gql_dict | networktocode.nautobot.graphql_string }}"
  vars:
    gql_dict:
      query:
        devices:
          name:
          primary_ip4:
            host:
          platform:
            napalm_driver:

# Output:
# ok: [localhost] => {
#     "ansible_facts": {
#         "gql_query": "query {\n  devices {\n    name\n    primary_ip4 {\n      host\n    }\n    platform {\n      napalm_driver\n    }\n  }\n}"
#     },
#     "changed": false
# }
"""


def build_graphql_filter_string(filter: dict) -> str:
    """Takes a dictionary and builds a graphql filter.

    Args:
        filter (dict): Key/Value pairs to build filter from

    Returns:
        str: Proper graphQL filter
    """
    base_filter = "({0})"
    loop_filters = []
    for key, value in filter.items():
        temp_string = f"{key}: "
        if isinstance(value, bool):
            # Convert Python booleans to lowercase
            value_string = str(value).lower()
        else:
            value_string = f"{value}"

        # GraphQL variables do not need quotes (This isn't completely support with inventory yet, but code added here)
        if isinstance(value, str) and not key.startswith("$"):
            value_string = "'" + value_string + "'"

        loop_filters.append(temp_string + value_string)

    return base_filter.format(", ".join(loop_filters))


def convert_to_graphql_string(query: dict, start=0) -> str:
    """Provide a dictionary to convert to a graphQL string.

    Args:
        query (dict): A dictionary mapping to the graphQL call to be made.
        start (int): The starting indentation when compiling string.

    Returns:
        str: GraphQL query string
    """
    graphql_string = """"""
    loop_index = 0
    query_len = len(query)
    for k, v in query.items():
        loop_index += 1
        loop_string = "".rjust(start * 2, " ")
        loop_filter = None

        # Determine what to do
        if not v:
            loop_string += f"{k}"
        elif isinstance(v, dict):
            if v.get("filters"):
                loop_filter = build_graphql_filter_string(v.pop("filters"))
            loop_string += "{0} {1}\n".format(k, loop_filter + " {" if loop_filter else "{")
            loop_string += convert_to_graphql_string(v, start + 1)
            loop_string += "{0}{1}".format(" " * (start * 2), "}")
        else:
            loop_string += "{0} {1}\n".format(k, "{")
            # We want to keep the double spaces, but add 2 more
            loop_string += "{0}".format(" " * (start * 2 + 2))
            loop_string += f"{v}\n"
            loop_string += "{0}{1}".format(" " * (start * 2), "}")

        if loop_index != query_len or start > 0:
            loop_string += "\n"

        graphql_string += loop_string

    return graphql_string.replace("'", '"')


class FilterModule:
    """Return graphQL filters."""

    def filters(self):
        """Map filter functions to filter names."""
        return {
            "graphql_string": convert_to_graphql_string,
        }
