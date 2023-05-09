# -*- coding: utf-8 -*-
# Copyright: (c) 2023, NTC (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NautobotModule


class NautobotPluginModule(NautobotModule):
    def run(self):
        """
        This function should have all necessary code for endpoints within the plugin application
        to create/update/delete the endpoint objects.
        """
        self.result = {"changed": False}
        data = self.data
        plugin_name = self.data["plugin"]
        endpoint_name = data["endpoint"]
        object_name = ", ".join(f"{key}:{value}" for key, value in self.data["id"].items())

        plugins_api = getattr(self.nb, self.endpoint)
        plugin_app = getattr(plugins_api, plugin_name)
        plugin_endpoint = getattr(plugin_app, endpoint_name)

        query_params = self.module.params.get("id")
        self.nb_object = self._nb_endpoint_get(plugin_endpoint, query_params, plugin_name)

        if self.module.params.get("attrs"):
            query_params.update(self.module.params["attrs"])
        if self.state == "present":
            self._ensure_object_exists(plugin_endpoint, endpoint_name, object_name, query_params)
        elif self.state == "absent":
            self._ensure_object_absent(endpoint_name, object_name)

        try:
            serialized_object = self.nb_object.serialize()
        except AttributeError:
            serialized_object = self.nb_object

        self.result[endpoint_name] = serialized_object

        self.module.exit_json(**self.result)
