#!/usr/bin/python
"""Base Action Plugin utilities."""
# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.plugins.connection import local as local_connection


class NBActionModule(ActionBase):
    """Module to be re-used by all modules to make these action modules with the benefits of regular modules, but execute locally."""

    def run(self, tmp=None, task_vars=None):
        module_args = self._task.args.copy()

        # We will change the connection to local to stick with the benefits of calling the module normally.
        if self._connection.transport != "local":
            self._connection = local_connection.Connection(self._play_context, self._connection._new_stdin)

        # We should be able to use this for all modules as the action should be valid to make dynamic and call proper module.
        # and we will account for non-FQDN being passed in.
        action_name = self._task.action if "networktocode.nautobot" in self._task.action else f"networktocode.nautobot.{self._task.action}"
        results = self._execute_module(module_name=action_name, module_args=module_args, task_vars=task_vars, tmp=tmp)

        return results
