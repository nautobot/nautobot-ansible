# -*- coding: utf-8 -*-
# Copyright: (c) 2025, Network to Code (@networktocode) <info@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    ENDPOINT_NAME_MAPPING,
    NautobotModule,
)

NB_MIN_MAX_RULES = "min_max_rules"
NB_REGEX_RULES = "regex_rules"
NB_REQUIRED_RULES = "required_rules"
NB_UNIQUE_RULES = "unique_rules"


class NautobotDataValidationModule(NautobotModule):
    def run(self):
        """Run the Nautobot Data Validation module.

        This function should have all necessary code for endpoints within the application
        to create/update/delete the endpoint objects
        Supported endpoints:
        - min_max_rules
        - regex_rules
        - required_rules
        - unique_rules
        """
        # Update the endpoint name to the Nautobot API endpoint name if it is different
        endpoint_name = ENDPOINT_NAME_MAPPING.get(self.endpoint, self.endpoint)

        self.result = {"changed": False}

        application = self._find_app(self.endpoint)
        nb_app = getattr(self.nb, application)
        nb_endpoint = getattr(nb_app, self.endpoint)
        user_query_params = self.module.params.get("query_params")

        data = self.data

        # Used for msg output
        if data.get("name"):
            name = data["name"]
        else:
            name = data.get("id")

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
