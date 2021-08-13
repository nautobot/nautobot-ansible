"""Nautobot Action Plugin to Query GraphQL."""

from __future__ import absolute_import, division, print_function

import os

from ansible.module_utils.six import raise_from
from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase

try:
    import pynautobot
except ImportError as imp_exc:
    PYNAUTOBOT_IMPORT_ERROR = imp_exc
else:
    PYNAUTOBOT_IMPORT_ERROR = None

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NautobotApiBase,
    NautobotGraphQL,
)
from ansible.utils.display import Display

__metaclass__ = type


def nautobot_action_graphql(args):
    """Ansible Action module execution for Nautobot query_graphql."""

    url = args.get("url") or os.getenv("NAUTOBOT_URL")
    Display().v("URL: %s" % url)

    # Verify URL is not None
    if url is None:
        raise AnsibleError("Missing URL of Nautobot")

    token = args.get("token") or os.getenv("NAUTOBOT_TOKEN")
    ssl_verify = args.get("validate_certs", True)
    Display().vv("Verify Certificates: %s" % ssl_verify)

    # Verify SSL Verify is of boolean
    if not isinstance(ssl_verify, bool):
        raise AnsibleError("validate_certs must be a boolean")

    nautobot_api = NautobotApiBase(token=token, url=url, ssl_verify=ssl_verify)
    query = args.get("query")
    Display().v("Query String: %s" % query)

    graph_variables = args.get("graph_variables")
    Display().v("Graph Variables: %s" % graph_variables)

    # Check that a valid query was passed in
    if query is None:
        raise AnsibleError(
            "Query parameter was not passed. Please verify that query is passed."
        )

    # Verify that the query is a string type
    if not isinstance(query, str):
        raise AnsibleError(
            "Query parameter must be of type string. Please see docs for examples."
        )

    # Verify that the variables key coming in is a dictionary
    if graph_variables is not None and not isinstance(graph_variables, dict):
        raise AnsibleError(
            "graph_variables parameter must be of key/value pairs. Please see docs for examples."
        )

    # Setup return results
    results = {"url": url, "query": query, "graph_variables": graph_variables}

    # Make call to Nautobot API and capture any failures
    nautobot_graph_obj = NautobotGraphQL(
        query_str=query, api=nautobot_api, variables=graph_variables
    )

    # Get the response from the object
    nautobot_response = nautobot_graph_obj.query()

    # Check for errors in the response
    if isinstance(nautobot_response, pynautobot.core.graphql.GraphQLException):
        raise AnsibleError(
            "Error in the query to the Nautobot host. Errors: %s"
            % (nautobot_response.errors)
        )

    # Good result, return it
    if isinstance(nautobot_response, pynautobot.core.graphql.GraphQLRecord):
        # Assign the data of a good result to the response
        results["data"] = nautobot_response.json.get("data")

    return results


class ActionModule(ActionBase):
    """Ansible Action Module to interact with Nautobot GraphQL Endpoint.

    Args:
        ActionBase (ActionBase): Ansible Action Plugin
    """

    def run(self, tmp=None, task_vars=None):
        """Run of action plugin for interacting with Nautobot GraphQL endpoint.

        Args:
            tmp ([type], optional): [description]. Defaults to None.
            task_vars ([type], optional): [description]. Defaults to None.
        """
        if PYNAUTOBOT_IMPORT_ERROR:
            raise_from(
                AnsibleError("pynautobot must be installed to use this plugin"),
                PYNAUTOBOT_IMPORT_ERROR,
            )

        self._supports_check_mode = False
        self._supports_async = False

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp

        if result.get("skipped"):
            return None

        if result.get("invocation", {}).get("module_args"):
            # avoid passing to modules in case of no_log
            # should not be set anymore but here for backwards compatibility
            del result["invocation"]["module_args"]

        # do work!
        # Get the arguments from the module definition
        args = self._task.args
        results = nautobot_action_graphql(args=args)

        # Results should be the data response of the query to be returned as a lookup
        return results
