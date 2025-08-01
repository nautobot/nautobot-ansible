# -*- coding: utf-8 -*-

# Copyright: (c) 2019. Chris Mills <chris@discreet-its.co.uk>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
A lookup function designed to return data from the Nautobot application.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    name: lookup
    author: Chris Mills (@cpmills1975)
    version_added: "1.0.0"
    short_description: Queries and returns elements from Nautobot
    description:
        - Queries Nautobot via its API to return virtually any information capable of being held in Nautobot.
    options:
        _terms:
            description:
                - The Nautobot object type to query
            required: True
        api_endpoint:
            description:
                - The URL to the Nautobot instance to query
            env:
                # in order of precedence
                - name: NAUTOBOT_URL
            required: True
        api_filter:
            description:
                - The api_filter to use.
            required: False
        api_version:
            description:
                - The Nautobot Rest API version to use.
            required: False
            version_added: "4.1.0"
        plugin:
            description:
                - The Nautobot plugin to query
            required: False
        token:
            description:
                - The API token created through Nautobot
                - This may not be required depending on the Nautobot setup.
            env:
                # in order of precendence
                - name: NAUTOBOT_TOKEN
            required: False
        validate_certs:
            description:
                - Whether or not to validate SSL of the Nautobot instance
            required: False
            default: True
        num_retries:
            description:
                - Number of retries
                - This will only affect HTTP codes 429, 500, 502, 503, and 504.
            required: False
            default: 0
        raw_data:
            description:
                - Whether to return raw API data with the lookup/query or whether to return a key/value dict
            required: False
    requirements:
        - pynautobot
"""

EXAMPLES = """
tasks:
  # query a list of devices
  - name: Obtain list of devices from Nautobot
    debug:
      msg: >
        "Device {{ item.value.display_name }} (ID: {{ item.key }}) was
         manufactured by {{ item.value.device_type.manufacturer.name }}"
    loop: "{{ query('networktocode.nautobot.lookup', 'devices',
                    api_endpoint='http://localhost/',
                    api_version='2.0',
                    token='<redacted>') }}"

# This example uses an API Filter
  # query a list of devices
  - name: Obtain list of devices from Nautobot
    debug:
      msg: >
        "Device {{ item.value.display_name }} (ID: {{ item.key }}) was
         manufactured by {{ item.value.device_type.manufacturer.name }}"
    loop: "{{ query('networktocode.nautobot.lookup', 'devices',
                    api_endpoint='http://localhost/',
                    api_version='2.0',
                    api_filter='role=management tags=Dell',
                    token='<redacted>') }}"

  # This example uses an API filter with depth set to get additional details from the lookup
  # Query a list of locations with API depth=1 to retrieve related details (like status, prefix_count, vlan_count)
  # Note: `location_name` should be set to the name of the desired location
  - name: Obtain location information from Nautobot and print some facts
    ansible.builtin.debug:
      msg: >-
        Location {{ item.value.name }} is {{ item.value['status']['name'] }} and has
        {{ item.value.prefix_count }} Prefixes and {{ item.value.vlan_count }} VLANs.
    loop: >-
      {{ query(
        'networktocode.nautobot.lookup',
        'locations',
        url=NAUTOBOT_URL,
        token=NAUTOBOT_TOKEN,
        api_filter='name=' + location_name + ' depth=1'
      ) }}

  # Fetch bgp sessions for R1-device
  - name: "Obtain bgp sessions for R1-Device"
    debug:
      msg: "{{ query('networktocode.nautobot.lookup', 'bgp_sessions',
                     api_filter='device=R1-Device',
                     api_endpoint='http://localhost/',
                     api_version='2.0',
                     token='<redacted>',
                     plugin='mycustomstuff') }}"
"""

RETURN = """
  _list:
    description:
      - list of composed dictionaries with key and value
    type: list
"""

import functools
import os
from pprint import pformat

from ansible.errors import AnsibleError
from ansible.module_utils.six import raise_from
from ansible.parsing.splitter import parse_kv, split_args
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    is_truthy,
)

try:
    import pynautobot
except ImportError as imp_exc:
    PYNAUTOBOT_IMPORT_ERROR = imp_exc
else:
    PYNAUTOBOT_IMPORT_ERROR = None


def get_endpoint(nautobot, term):
    """Get the endpoint for the given term.

    Args:
        nautobot (pynautobot.api): a predefined pynautobot.api() pointing to a valid instance of Nautobot
        term (str): the term passed to the lookup function upon which the api call will be identified

    Returns:
        dict: The endpoint for the given term.
    """
    endpoint_map = {
        "admin-users": {"endpoint": nautobot.users.users},
        "admin-groups": {"endpoint": nautobot.users.groups},
        "admin-permissions": {"endpoint": nautobot.users.permissions},
        "aggregates": {"endpoint": nautobot.ipam.aggregates},
        "circuit-terminations": {"endpoint": nautobot.circuits.circuit_terminations},
        "circuit-types": {"endpoint": nautobot.circuits.circuit_types},
        "circuits": {"endpoint": nautobot.circuits.circuits},
        "circuit-providers": {"endpoint": nautobot.circuits.providers},
        "cables": {"endpoint": nautobot.dcim.cables},
        "controllers": {"endpoint": nautobot.dcim.controllers},
        "controller-managed-device-groups": {"endpoint": nautobot.dcim.controller_managed_device_groups},
        "cloud-accounts": {"endpoint": nautobot.cloud.cloud_accounts},
        "cloud-networks": {"endpoint": nautobot.cloud.cloud_networks},
        "cloud-network-prefix-assignments": {"endpoint": nautobot.cloud.cloud_network_prefix_assignments},
        "cloud-resource-types": {"endpoint": nautobot.cloud.cloud_resource_types},
        "cloud-services": {"endpoint": nautobot.cloud.cloud_services},
        "cloud-service-network-assignments": {"endpoint": nautobot.cloud.cloud_service_network_assignments},
        "cluster-groups": {"endpoint": nautobot.virtualization.cluster_groups},
        "cluster-types": {"endpoint": nautobot.virtualization.cluster_types},
        "clusters": {"endpoint": nautobot.virtualization.clusters},
        "config-contexts": {"endpoint": nautobot.extras.config_contexts},
        "console-connections": {"endpoint": nautobot.dcim.console_connections},
        "console-ports": {"endpoint": nautobot.dcim.console_ports},
        "console-server-port-templates": {"endpoint": nautobot.dcim.console_server_port_templates},
        "console-server-ports": {"endpoint": nautobot.dcim.console_server_ports},
        "contacts": {"endpoint": nautobot.extras.contacts},
        "custom-fields": {"endpoint": nautobot.extras.custom_fields},
        "custom-field-choices": {"endpoint": nautobot.extras.custom_field_choices},
        "device-bay-templates": {"endpoint": nautobot.dcim.device_bay_templates},
        "device-bays": {"endpoint": nautobot.dcim.device_bays},
        "device-types": {"endpoint": nautobot.dcim.device_types},
        "device-redundancy-groups": {"endpoint": nautobot.dcim.device_redundancy_groups},
        "devices": {"endpoint": nautobot.dcim.devices},
        "dynamic-groups": {"endpoint": nautobot.extras.dynamic_groups},
        "export-templates": {"endpoint": nautobot.dcim.export_templates},
        "front-port-templates": {"endpoint": nautobot.dcim.front_port_templates},
        "front-ports": {"endpoint": nautobot.dcim.front_ports},
        "graphs": {"endpoint": nautobot.extras.graphs},
        "image-attachments": {"endpoint": nautobot.extras.image_attachments},
        "interface-connections": {"endpoint": nautobot.dcim.interface_connections},
        "interface-templates": {"endpoint": nautobot.dcim.interface_templates},
        "interfaces": {"endpoint": nautobot.dcim.interfaces},
        "inventory-items": {"endpoint": nautobot.dcim.inventory_items},
        "ip-addresses": {"endpoint": nautobot.ipam.ip_addresses},
        "ip-address-to-interface": {"endpoint": nautobot.ipam.ip_address_to_interface},
        "job-buttons": {"endpoint": nautobot.extras.job_buttons},
        "jobs": {"endpoint": nautobot.extras.jobs},
        "locations": {"endpoint": nautobot.dcim.locations},
        "location-types": {"endpoint": nautobot.dcim.location_types},
        "manufacturers": {"endpoint": nautobot.dcim.manufacturers},
        "metadata-choices": {"endpoint": nautobot.extras.metadata_choices},
        "metadata-types": {"endpoint": nautobot.extras.metadata_types},
        "module-bay-templates": {"endpoint": nautobot.dcim.module_bay_templates},
        "module-bays": {"endpoint": nautobot.dcim.module_bays},
        "module-types": {"endpoint": nautobot.dcim.module_types},
        "modules": {"endpoint": nautobot.dcim.modules},
        "namespaces": {"endpoint": nautobot.ipam.namespaces},
        "object-changes": {"endpoint": nautobot.extras.object_changes},
        "object-metadata": {"endpoint": nautobot.extras.object_metadata},
        "platforms": {"endpoint": nautobot.dcim.platforms},
        "power-connections": {"endpoint": nautobot.dcim.power_connections},
        "power-outlet-templates": {"endpoint": nautobot.dcim.power_outlet_templates},
        "power-outlets": {"endpoint": nautobot.dcim.power_outlets},
        "power-panels": {"endpoint": nautobot.dcim.power_panels},
        "power-port-templates": {"endpoint": nautobot.dcim.power_port_templates},
        "power-ports": {"endpoint": nautobot.dcim.power_ports},
        "prefixes": {"endpoint": nautobot.ipam.prefixes},
        "prefix-location-assignments": {"endpoint": nautobot.ipam.prefix_location_assignments},
        "provider-networks": {"endpoint": nautobot.circuits.provider_networks},
        "rack-groups": {"endpoint": nautobot.dcim.rack_groups},
        "rack-reservations": {"endpoint": nautobot.dcim.rack_reservations},
        "racks": {"endpoint": nautobot.dcim.racks},
        "radio-profiles": {"endpoint": nautobot.wireless.radio_profiles},
        "rear-port-templates": {"endpoint": nautobot.dcim.rear_port_templates},
        "rear-ports": {"endpoint": nautobot.dcim.rear_ports},
        "relationships": {"endpoint": nautobot.extras.relationships},
        "relationship-associations": {"endpoint": nautobot.extras.relationship_associations},
        "reports": {"endpoint": nautobot.extras.reports},
        "rirs": {"endpoint": nautobot.ipam.rirs},
        "roles": {"endpoint": nautobot.extras.roles},
        "secrets": {"endpoint": nautobot.extras.secrets},
        "secrets-groups": {"endpoint": nautobot.extras.secrets_groups},
        "secrets-groups-associations": {"endpoint": nautobot.extras.secrets_groups_associations},
        "services": {"endpoint": nautobot.ipam.services},
        "software-image-files": {"endpoint": nautobot.dcim.software_image_files},
        "software-versions": {"endpoint": nautobot.dcim.software_versions},
        "static-group-associations": {"endpoint": nautobot.extras.static_group_associations},
        "statuses": {"endpoint": nautobot.extras.statuses},
        "supported-data-rates": {"endpoint": nautobot.wireless.supported_data_rates},
        "tags": {"endpoint": nautobot.extras.tags},
        "teams": {"endpoint": nautobot.extras.teams},
        "tenant-groups": {"endpoint": nautobot.tenancy.tenant_groups},
        "tenants": {"endpoint": nautobot.tenancy.tenants},
        "topology-maps": {"endpoint": nautobot.extras.topology_maps},
        "virtual-chassis": {"endpoint": nautobot.dcim.virtual_chassis},
        "virtual-machines": {"endpoint": nautobot.virtualization.virtual_machines},
        "virtualization-interfaces": {"endpoint": nautobot.virtualization.interfaces},
        "vlan-groups": {"endpoint": nautobot.ipam.vlan_groups},
        "vlans": {"endpoint": nautobot.ipam.vlans},
        "vlan-location-assignments": {"endpoint": nautobot.ipam.vlan_location_assignments},
        "vrfs": {"endpoint": nautobot.ipam.vrfs},
        "wireless-networks": {"endpoint": nautobot.wireless.wireless_networks},
    }

    return endpoint_map[term]["endpoint"]


def build_filters(filters):
    """
    This will build the filters to be handed to Nautobot endpoint call if they exist.

    Args:
        filters (str): String of filters to parse.

    Returns:
        result (list): List of dictionaries to filter by.
    """
    filter = {}
    args_split = split_args(filters)
    args = [parse_kv(x) for x in args_split]
    for arg in args:
        for k, v in arg.items():
            if k not in filter:
                filter[k] = list()
                filter[k].append(v)
            else:
                filter[k].append(v)

    return filter


def get_plugin_endpoint(nautobot, plugin, term):
    """Get the plugin endpoint for the given plugin and term.

    Args:
        nautobot (pynautobot.api): a predefined pynautobot.api() pointing to a valid instance of Nautobot
        plugin (str): a string referencing the plugin name
        term (str): the term passed to the lookup function upon which the api call will be identified

    Returns:
        object: The plugin endpoint for the given plugin and term.
    """
    attr = "plugins.%s.%s" % (plugin, term)

    def _getattr(nautobot, attr):
        return getattr(nautobot, attr)

    return functools.reduce(_getattr, [nautobot] + attr.split("."))


def make_call(endpoint, filters=None):  # noqa: D417
    """
    Wrapper for calls to Nautobot and handle any possible errors.

    Args:
        endpoint (object): The Nautobot endpoint object to make calls.

    Returns:
        results (object): Pynautobot result.

    Raises:
        AnsibleError: Ansible Error containing an error message.
    """
    try:
        if filters:
            results = endpoint.filter(**filters)
        else:
            results = endpoint.all()
    except pynautobot.RequestError as e:
        if e.req.status_code == 404 and "plugins" in e:
            raise AnsibleError(
                f"{e.error} - Not a valid plugin endpoint, please make sure to provide valid plugin endpoint."
            )
        else:
            raise AnsibleError(e.error)

    return results


class LookupModule(LookupBase):
    """
    LookupModule(LookupBase) is defined by Ansible.
    """

    def run(self, terms, variables=None, **kwargs):
        """Run the lookup."""
        if PYNAUTOBOT_IMPORT_ERROR:
            raise_from(
                AnsibleError("pynautobot must be installed to use this plugin"),
                PYNAUTOBOT_IMPORT_ERROR,
            )

        api_token = kwargs.get("token") or os.getenv("NAUTOBOT_TOKEN")
        api_endpoint = kwargs.get("api_endpoint") or os.getenv("NAUTOBOT_URL")
        if not api_endpoint or not api_token:
            raise AnsibleError("Both api_endpoint and token are required")
        if kwargs.get("validate_certs") is not None:
            ssl_verify = kwargs.get("validate_certs")
        elif os.getenv("NAUTOBOT_VALIDATE_CERTS") is not None:
            ssl_verify = is_truthy(os.getenv("NAUTOBOT_VALIDATE_CERTS"))
        else:
            ssl_verify = True
        num_retries = kwargs.get("num_retries", "0")
        api_filter = kwargs.get("api_filter")
        if api_filter:
            api_filter = self._templar.do_template(api_filter)
        raw_return = kwargs.get("raw_data")
        plugin = kwargs.get("plugin")
        api_version = kwargs.get("api_version")

        if not isinstance(terms, list):
            terms = [terms]

        nautobot = pynautobot.api(
            api_endpoint,
            token=api_token if api_token else None,
            api_version=api_version,
            verify=ssl_verify,
            retries=num_retries,
        )
        results = []
        for term in terms:
            if plugin:
                endpoint = get_plugin_endpoint(nautobot, plugin, term)
            else:
                try:
                    endpoint = get_endpoint(nautobot, term)
                except KeyError:
                    raise AnsibleError("Unrecognised term %s. Check documentation" % term)

            Display().vvvv(
                "Nautobot lookup for %s to %s using token %s filter %s" % (term, api_endpoint, api_token, api_filter)
            )

            if api_filter:
                filter = build_filters(api_filter)
                Display().vvvv("filter is %s" % filter)

            # Make call to Nautobot API and capture any failures
            response = make_call(endpoint, filters=filter if api_filter else None)

            for data in response:
                data = dict(data)
                Display().vvvvv(pformat(data))

                if raw_return:
                    results.append(data)
                else:
                    key = data["id"]
                    result = {key: data}
                    results.extend(self._flatten_hash_to_list(result))

        return results
