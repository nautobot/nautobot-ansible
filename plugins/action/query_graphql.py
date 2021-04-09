"""Nautobot Action Plugin to Query GraphQL."""

from __future__ import absolute_import, division, print_function
from ..module_utils.utils import NautobotApiBase, NautobotGraphQL

__metaclass__ = type

from ansible.plugins.action import ActionBase

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

        token = args.get("token") or os.getenv("NAUTOBOT_TOKEN")
        url = args.get("url") or os.getenv("NAUTOBOT_URL")
        ssl_verify = args.get("validate_certs", True)
        nautobot_api = NautobotApiBase(token=token, url=url, ssl_verify=ssl_verify)
        query = args.get("query")
        variables = args.get("variables")

        # Setup return results
        results = {}
        # Make call to Nautobot API and capture any failures
        nautobot_graph_obj = NautobotGraphQL(
            query=query, api=nautobot_api, variables=variables
        )

        # Add data for the return
        results["data"] = nautobot_graph_obj.query()

        # Results should be the data response of the query to be returned as a lookup
        return results
