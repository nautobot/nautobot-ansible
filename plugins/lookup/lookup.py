# -*- coding: utf-8 -*-

# Copyright: (c) 2019. Chris Mills <chris@discreet-its.co.uk>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
"""
nautobot.py

A lookup function designed to return data from the Nautobot application
"""

from __future__ import absolute_import, division, print_function

import os
import functools
from pprint import pformat

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.parsing.splitter import parse_kv, split_args
from ansible.utils.display import Display

import pynautobot
import requests

__metaclass__ = type

DOCUMENTATION = """
    lookup: lookup
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
                    token='<redacted>') }}"

# This example uses an API Filter
tasks:
  # query a list of devices
  - name: Obtain list of devices from Nautobot
    debug:
      msg: >
        "Device {{ item.value.display_name }} (ID: {{ item.key }}) was
         manufactured by {{ item.value.device_type.manufacturer.name }}"
    loop: "{{ query('networktocode.nautobot.lookup', 'devices',
                    api_endpoint='http://localhost/',
                    api_filter='role=management tag=Dell'),
                    token='<redacted>') }}"

# Fetch bgp sessions for R1-device
tasks:
  - name: "Obtain bgp sessions for R1-Device"
    debug:
      msg: "{{ query('networktocode.nautobot.lookup', 'bgp_sessions',
                     api_filter='device=R1-Device',
                     api_endpoint='http://localhost/',
                     token='<redacted>',
                     plugin='mycustomstuff') }}"
"""

RETURN = """
  _list:
    description:
      - list of composed dictionaries with key and value
    type: list
"""


def get_endpoint(nautobot, term):
    """
    get_endpoint(nautobot, term)
        nautobot: a predefined pynautobot.api() pointing to a valid instance
                of Nautobot
        term: the term passed to the lookup function upon which the api
              call will be identified
    """

    endpoint_map = {
        "aggregates": {"endpoint": nautobot.ipam.aggregates},
        "circuit-terminations": {"endpoint": nautobot.circuits.circuit_terminations},
        "circuit-types": {"endpoint": nautobot.circuits.circuit_types},
        "circuits": {"endpoint": nautobot.circuits.circuits},
        "circuit-providers": {"endpoint": nautobot.circuits.providers},
        "cables": {"endpoint": nautobot.dcim.cables},
        "cluster-groups": {"endpoint": nautobot.virtualization.cluster_groups},
        "cluster-types": {"endpoint": nautobot.virtualization.cluster_types},
        "clusters": {"endpoint": nautobot.virtualization.clusters},
        "config-contexts": {"endpoint": nautobot.extras.config_contexts},
        "console-connections": {"endpoint": nautobot.dcim.console_connections},
        "console-ports": {"endpoint": nautobot.dcim.console_ports},
        "console-server-port-templates": {
            "endpoint": nautobot.dcim.console_server_port_templates
        },
        "console-server-ports": {"endpoint": nautobot.dcim.console_server_ports},
        "device-bay-templates": {"endpoint": nautobot.dcim.device_bay_templates},
        "device-bays": {"endpoint": nautobot.dcim.device_bays},
        "device-roles": {"endpoint": nautobot.dcim.device_roles},
        "device-types": {"endpoint": nautobot.dcim.device_types},
        "devices": {"endpoint": nautobot.dcim.devices},
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
        "manufacturers": {"endpoint": nautobot.dcim.manufacturers},
        "object-changes": {"endpoint": nautobot.extras.object_changes},
        "platforms": {"endpoint": nautobot.dcim.platforms},
        "power-connections": {"endpoint": nautobot.dcim.power_connections},
        "power-outlet-templates": {"endpoint": nautobot.dcim.power_outlet_templates},
        "power-outlets": {"endpoint": nautobot.dcim.power_outlets},
        "power-panels": {"endpoint": nautobot.dcim.power_panels},
        "power-port-templates": {"endpoint": nautobot.dcim.power_port_templates},
        "power-ports": {"endpoint": nautobot.dcim.power_ports},
        "prefixes": {"endpoint": nautobot.ipam.prefixes},
        "rack-groups": {"endpoint": nautobot.dcim.rack_groups},
        "rack-reservations": {"endpoint": nautobot.dcim.rack_reservations},
        "rack-roles": {"endpoint": nautobot.dcim.rack_roles},
        "racks": {"endpoint": nautobot.dcim.racks},
        "rear-port-templates": {"endpoint": nautobot.dcim.rear_port_templates},
        "rear-ports": {"endpoint": nautobot.dcim.rear_ports},
        "regions": {"endpoint": nautobot.dcim.regions},
        "reports": {"endpoint": nautobot.extras.reports},
        "rirs": {"endpoint": nautobot.ipam.rirs},
        "roles": {"endpoint": nautobot.ipam.roles},
        "services": {"endpoint": nautobot.ipam.services},
        "sites": {"endpoint": nautobot.dcim.sites},
        "statuses": {"endpoint": nautobot.extras.statuses},
        "tags": {"endpoint": nautobot.extras.tags},
        "tenant-groups": {"endpoint": nautobot.tenancy.tenant_groups},
        "tenants": {"endpoint": nautobot.tenancy.tenants},
        "topology-maps": {"endpoint": nautobot.extras.topology_maps},
        "virtual-chassis": {"endpoint": nautobot.dcim.virtual_chassis},
        "virtual-machines": {"endpoint": nautobot.virtualization.virtual_machines},
        "virtualization-interfaces": {"endpoint": nautobot.virtualization.interfaces},
        "vlan-groups": {"endpoint": nautobot.ipam.vlan_groups},
        "vlans": {"endpoint": nautobot.ipam.vlans},
        "vrfs": {"endpoint": nautobot.ipam.vrfs},
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
    """
    get_plugin_endpoint(nautobot, plugin, term)
        nautobot: a predefined pynautobot.api() pointing to a valid instance
                of Nautobot
        plugin: a string referencing the plugin name
        term: the term passed to the lookup function upon which the api
              call will be identified
    """
    attr = "plugins.%s.%s" % (plugin, term)

    def _getattr(nautobot, attr):
        return getattr(nautobot, attr)

    return functools.reduce(_getattr, [nautobot] + attr.split("."))


def make_call(endpoint, filters=None):
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
                "{0} - Not a valid plugin endpoint, please make sure to provide valid plugin endpoint.".format(
                    e.error
                )
            )
        else:
            raise AnsibleError(e.error)

    return results


class LookupModule(LookupBase):
    """
    LookupModule(LookupBase) is defined by Ansible
    """

    def run(self, terms, variables=None, **kwargs):

        api_token = kwargs.get("token") or os.getenv("NAUTOBOT_TOKEN")
        api_endpoint = kwargs.get("api_endpoint") or os.getenv("NAUTOBOT_URL")
        ssl_verify = kwargs.get("validate_certs", True)
        api_filter = kwargs.get("api_filter")
        raw_return = kwargs.get("raw_data")
        plugin = kwargs.get("plugin")

        if not isinstance(terms, list):
            terms = [terms]

        session = requests.Session()
        session.verify = ssl_verify

        nautobot = pynautobot.api(api_endpoint, token=api_token if api_token else None,)
        nautobot.http_session = session

        results = []
        for term in terms:
            if plugin:
                endpoint = get_plugin_endpoint(nautobot, plugin, term)
            else:
                try:
                    endpoint = get_endpoint(nautobot, term)
                except KeyError:
                    raise AnsibleError(
                        "Unrecognised term %s. Check documentation" % term
                    )

            Display().vvvv(
                u"Nautobot lookup for %s to %s using token %s filter %s"
                % (term, api_endpoint, api_token, api_filter)
            )

            if api_filter:
                filter = build_filters(api_filter)

                if "id" in filter:
                    Display().vvvv(
                        u"Filter is: %s and includes id, will use .get instead of .filter"
                        % (filter)
                    )
                    try:
                        id = int(filter["id"][0])
                        data = endpoint.get(id)
                        data = dict(data)
                        Display().vvvvv(pformat(data))
                        return [data]
                    except pynautobot.RequestError as e:
                        raise AnsibleError(e.error)

                Display().vvvv("filter is %s" % filter)

            # Make call to Nautobot API and capture any failures
            data = make_call(endpoint, filters=filter if api_filter else None)

            for data in data:
                data = dict(data)
                Display().vvvvv(pformat(data))

                if raw_return:
                    results.append(data)
                else:
                    key = data["id"]
                    result = {key: data}
                    results.extend(self._flatten_hash_to_list(result))

        return results
