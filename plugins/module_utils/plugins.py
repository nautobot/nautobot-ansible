# -*- coding: utf-8 -*-
# Copyright: (c) 2023, NTC (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NautobotModule


class NautobotPluginModule(NautobotModule):
    def run(self):
        """Run the Nautobot plugin module.

        This function should have all necessary code for endpoints within the plugin application
        to create/update/delete the endpoint objects.
        """
        self.result = {"changed": False}
        plugin_name = self.data["plugin"]
        endpoint_name = self.data["endpoint"]
        object_name = ", ".join(f"{key}:{value}" for key, value in self.data["identifiers"].items())
        user_query_params = self.module.params.get("query_params")

        plugins_api = getattr(self.nb, self.endpoint)
        plugin_app = getattr(plugins_api, plugin_name)
        plugin_endpoint = getattr(plugin_app, endpoint_name)

        # Prepare object attributes to be data parent keys.
        data = self.module.params.get("identifiers").copy()
        if self.module.params.get("attrs"):
            data.update(self.module.params["attrs"])

        if not user_query_params:
            user_query_params = self.module.params.get("identifiers")

        # Need to call _find_ids again, despite it's part of __init__ because plugin module has object attrs as child keys.
        data = self._find_ids(data, user_query_params)

        object_query_params = self._build_query_params(endpoint_name, data, user_query_params=user_query_params)
        self.nb_object = self._nb_endpoint_get(plugin_endpoint, object_query_params, plugin_name)

        if self.state == "present":
            self._ensure_object_exists(plugin_endpoint, endpoint_name, object_name, data)
        elif self.state == "absent":
            self._ensure_object_absent(endpoint_name, object_name)

        try:
            serialized_object = self.nb_object.serialize()
        except AttributeError:
            serialized_object = self.nb_object

        self.result[endpoint_name] = serialized_object

        self.module.exit_json(**self.result)
