# -*- coding: utf-8 -*-
# Copyright: (c) 2024, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    ENDPOINT_NAME_MAPPING,
    NautobotModule,
)

NB_CLOUD_SERVICES = "cloud_services"
NB_CLOUD_NETWORKS = "cloud_networks"
NB_CLOUD_NETWORK_PREFIX_ASSIGNMENTS = "cloud_network_prefix_assignments"
NB_CLOUD_SERVICE_NETWORK_ASSIGNMENTS = "cloud_service_network_assignments"
NB_CLOUD_ACCOUNTS = "cloud_accounts"
NB_CLOUD_RESOURCE_TYPES = "cloud_resource_types"


class NautobotCloudModule(NautobotModule):
    def run(self):
        """Run the Nautobot Cloud module.

        This function should have all necessary code for endpoints within the application
        to create/update/delete the endpoint objects
        Supported endpoints:
        - cloud_services
        - cloud_networks
        - cloud_network_prefix_assignments
        - cloud_service_network_assignments
        - cloud_accounts
        - cloud_resource_types
        """
        # Used to dynamically set key when returning results
        endpoint_name = ENDPOINT_NAME_MAPPING[self.endpoint]

        self.result = {"changed": False}

        application = self._find_app(self.endpoint)
        nb_app = getattr(self.nb, application)
        nb_endpoint = getattr(nb_app, self.endpoint)
        user_query_params = self.module.params.get("query_params")

        data = self.data

        # Used for msg output
        if data.get("name"):
            name = data["name"]
        elif endpoint_name == "cloud_service_network_assignment":
            cloud_service = self.module.params["cloud_service"]
            cloud_network = self.module.params["cloud_network"]

            name = "%s <> %s" % (
                cloud_service,
                cloud_network,
            )
        elif endpoint_name == "cloud_network_prefix_assignment":
            cloud_network = self.module.params["cloud_network"]
            cloud_prefix = self.module.params["cloud_prefix"]

            name = "%s <> %s" % (cloud_network, cloud_prefix)

        object_query_params = self._build_query_params(endpoint_name, data, user_query_params)
        self.nb_object = self._nb_endpoint_get(nb_endpoint, object_query_params, name)

        if self.state == "present":
            self._ensure_object_exists(nb_endpoint, endpoint_name, name, data)
        elif self.state == "absent":
            self._ensure_object_absent(endpoint_name, name)

        try:
            serialized_object = self.nb_object.serialize()
        except AttributeError:
            serialized_object = self.nb_object

        self.result.update({endpoint_name: serialized_object})

        self.module.exit_json(**self.result)
