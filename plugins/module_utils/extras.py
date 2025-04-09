# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@fragmentedpacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NautobotModule,
    ENDPOINT_NAME_MAPPING,
)

NB_DYNAMIC_GROUPS = "dynamic_groups"
NB_TAGS = "tags"
NB_STATUS = "statuses"
NB_RELATIONSHIP_ASSOCIATIONS = "relationship_associations"
NB_STATIC_GROUP_ASSOCIATIONS = "static_group_associations"
NB_CUSTOM_FIELDS = "custom_fields"
NB_CUSTOM_FIELD_CHOICES = "custom_field_choices"
NB_CONTACT = "contacts"
NB_TEAM = "teams"
NB_JOB_BUTTONS = "job_buttons"
NB_OBJECT_METADATA = "object_metadata"
NB_METADATA_CHOICES = "metadata_choices"
NB_METADATA_TYPES = "metadata_types"
NB_SECRET = "secrets"  # nosec B105
NB_SECRETS_GROUP = "secrets_groups"


class NautobotExtrasModule(NautobotModule):
    def run(self):
        """
        This function should have all necessary code for endpoints within the application
        to create/update/delete the endpoint objects
        Supported endpoints:
        - tags
        - statuses
        - relationship_associations
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
        elif endpoint_name == "relationship_associations":
            name = f"{data['source_type']} -> {data['destination_type']}"
        elif endpoint_name == "static_group_association":
            name = f"{data['dynamic_group']} -> {data['associated_object_id']}"
        elif endpoint_name == "custom_field":
            name = data["label"]
        elif endpoint_name in ["custom_field_choice", "metadata_choice"]:
            name = data["value"]
        elif endpoint_name in ["object_metadata"]:
            name = data.get("value", data.get("contact", data.get("team")))
        else:
            name = data.get("id")

        # Make color params lowercase
        if data.get("color"):
            data["color"] = data["color"].lower()

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
