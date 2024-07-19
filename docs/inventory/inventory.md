# networktocode.nautobot.inventory

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.inventory`.

## Synopsis

- Get inventory hosts from Nautobot


## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| ansible_host_dns_name | boolean |  | If True, sets DNS Name (fetched from primary_ip) to be used in ansible_host variable, instead of IP Address. |
| api_endpoint |  |  | Endpoint of the Nautobot API |
| api_version |  | 4.1.0 | The version of the Nautobot REST API. |
| cache | bool |  | Toggle to enable/disable the caching of the inventory's source data, requires a cache plugin setup to work. |
| cache_connection | str |  | Cache connection data or path, read cache plugin documentation for specifics. |
| cache_plugin | str |  | Cache plugin to use for the inventory's source data. |
| cache_prefix |  |  | Prefix to use for cache plugin files/tables |
| cache_timeout | int |  | Cache duration in seconds |
| compose | dict |  | List of custom ansible host vars to create from the device object fetched from Nautobot |
| config_context | boolean |  | If True, it adds config_context in host vars. Config-context enables the association of arbitrary data to devices and virtual machines grouped by location, role, platform, and/or tenant. Please check official nautobot docs for more info. |
| device_query_filters | list |  | List of parameters passed to the query string for devices (Multiple values may be separated by commas) |
| dns_name | boolean |  | Force IP Addresses to be fetched so that the dns_name for the primary_ip of each device or VM is set as a host_var. Setting interfaces will also fetch IP addresses and the dns_name host_var will be set. |
| fetch_all | boolean | 1.0.0 | By default, fetching interfaces and services will get all of the contents of Nautobot regardless of query_filters applied to devices and VMs. When set to False, separate requests will be made fetching interfaces, services, and IP addresses for each device_id and virtual_machine_id. If you are using the various query_filters options to reduce the number of devices, querying Nautobot may be faster with fetch_all False. For efficiency, when False, these requests will be batched, for example /api/dcim/interfaces?limit=0&device_id=1&device_id=2&device_id=3 These GET request URIs can become quite large for a large number of devices. If you run into HTTP 414 errors, you can adjust the max_uri_length option to suit your web server. |
| flatten_config_context | boolean | 1.0.0 | If I(config_context) is enabled, by default it's added as a host var named config_context. If flatten_config_context is set to True, the config context variables will be added directly to the host instead. |
| flatten_custom_fields | boolean | 1.0.0 | By default, host custom fields are added as a dictionary host var named custom_fields. If flatten_custom_fields is set to True, the fields will be added directly to the host instead. |
| flatten_local_context_data | boolean | 1.0.0 | If I(local_context_data) is enabled, by default it's added as a host var named local_context_data. If flatten_local_context_data is set to True, the config context variables will be added directly to the host instead. |
| follow_redirects |  |  | Determine how redirects are followed. By default, I(follow_redirects) is set to uses urllib2 default behavior. |
| group_by | list |  | Keys used to create groups. The I(plurals) option controls which of these are valid. |
| group_names_raw | boolean | 1.0.0 | Will not add the group_by choice name to the group names |
| groups | dict |  | Add hosts to group based on Jinja2 conditionals. |
| interfaces | boolean | 1.0.0 | If True, it adds the device or virtual machine interface information in host vars. |
| keyed_groups | list |  | Add hosts to group based on the values of a variable. |
| leading_separator | boolean | 2.11 | Use in conjunction with keyed_groups. By default, a keyed group that does not have a prefix or a separator provided will have a name that starts with an underscore. This is because the default prefix is "" and the default separator is "_". Set this option to False to omit the leading underscore (or other separator) if no prefix is given. If the group name is derived from a mapping the separator is still used to concatenate the items. To not use a separator in the group name at all, set the separator for the keyed group to an empty string instead. |
| max_uri_length | int | 1.0.0 | When fetch_all is False, GET requests to Nautobot may become quite long and return a HTTP 414 (URI Too Long). You can adjust this option to be smaller to avoid 414 errors, or larger for a reduced number of requests. |
| plugin |  |  | token that ensures this is a source file for the 'nautobot' plugin. |
| plurals | boolean | 1.0.0 | If True, all host vars are contained inside single-element arrays for legacy compatibility with old versions of this plugin. Group names will be plural (ie. "locations_mylocation" instead of "location_mylocation") The choices of I(group_by) will be changed by this option. |
| query_filters | list |  | List of parameters passed to the query string for both devices and VMs (Multiple values may be separated by commas) |
| services | boolean | 1.0.0 | If True, it adds the device or virtual machine services information in host vars. |
| strict | bool |  | If C(yes) make invalid entries a fatal error, otherwise skip and continue. Since it is possible to use facts in the expressions they might not always be available and we ignore those errors by default. |
| timeout | int |  | Timeout for Nautobot requests in seconds |
| token |  |  | Nautobot API token to be able to read against Nautobot. This may not be required depending on the Nautobot setup. |
| use_extra_vars | bool | 2.11 | Merge extra vars into the available variables for composition (highest precedence). |
| validate_certs | boolean |  | Allows connection when SSL certificates are not valid. Set to C(false) when certificates are not trusted. |
| virtual_chassis_name | boolean |  | When a device is part of a virtual chassis, use the virtual chassis name as the Ansible inventory hostname. The host var values will be from the virtual chassis master. |
| vm_query_filters | list |  | List of parameters passed to the query string for VMs (Multiple values may be separated by commas) |


## Examples

```yaml

# inventory.yml file in YAML format
# Example command line: ansible-inventory -v --list -i inventory.yml

plugin: networktocode.nautobot.inventory
api_endpoint: http://localhost:8000
validate_certs: True
config_context: False
group_by:
  - device_roles
query_filters:
  - role: network-edge-router
device_query_filters:
  - has_primary_ip: 'true'

# has_primary_ip is a useful way to filter out patch panels and other passive devices

# Query filters are passed directly as an argument to the fetching queries.
# You can repeat tags in the query string.

query_filters:
  - role: server
  - tag: web
  - tag: production

# See the Nautobot documentation at https://nautobot.readthedocs.io/en/latest/api/overview/
# the query_filters work as a logical **OR**
#
# Prefix any custom fields with cf_ and pass the field value with the regular Nautobot query string

query_filters:
  - cf_foo: bar

# Nautobot inventory plugin also supports Constructable semantics
# You can fill your hosts vars using the compose option:

plugin: networktocode.nautobot.inventory
compose:
  foo: last_updated
  bar: display
  nested_variable: rack.display

# You can use keyed_groups to group on properties of devices or VMs.
# NOTE: It's only possible to key off direct items on the device/VM objects.
plugin: networktocode.nautobot.inventory
keyed_groups:
  - prefix: status
    key: status.value

```


## Authors

- Remy Leone (@sieben)
- Anthony Ruhier (@Anthony25)
- Nikhil Singh Baliyan (@nikkytub)
- Sander Steffann (@steffann)
- Douglas Heriot (@DouglasHeriot)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
