# -*- coding: utf-8 -*-


from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NautobotModule,
    ENDPOINT_NAME_MAPPING,
    SLUG_REQUIRED,
)


NB_TENANTS = "tenants"
NB_TENANT_GROUPS = "tenant_groups"


class NautobotTenancyModule(NautobotModule):
    def __init__(self, module, endpoint, client=None, remove_keys=None):
        super().__init__(module, endpoint, client, remove_keys)

    def run(self):
        """
        This function should have all necessary code for endpoints within the application
        to create/update/delete the endpoint objects
        Supported endpoints:
        tenants
        tenant groups
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
        elif data.get("slug"):
            name = data["slug"]

        if self.endpoint in SLUG_REQUIRED:
            if not data.get("slug"):
                data["slug"] = self._to_slug(name)

        object_query_params = self._build_query_params(
            endpoint_name, data, user_query_params
        )
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
