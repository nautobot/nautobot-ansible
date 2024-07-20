# networktocode.nautobot.gql_inventory

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install the collection, use: 
    
    ```
    ansible-galaxy collection install networktocode.nautobot
    ```
    
    You need further requirements to be able to use this module, see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.gql_inventory`.

## Synopsis

- Get inventory hosts from Nautobot using GraphQL queries

## Requirements

The below requirements are needed on the host that executes this module.

- netutils

## Parameters

| Parameter | Data Type | Environment Variable | Version Added | Comments |
| --------- | --------- | -------------------- | ------------- | -------- |
| api_endpoint |  |  NAUTOBOT_URL  |  | Endpoint of the Nautobot API |
| cache | bool |  ANSIBLE_INVENTORY_CACHE  |  | Toggle to enable/disable the caching of the inventory's source data, requires a cache plugin setup to work. |
| cache_connection | str |  ANSIBLE_CACHE_PLUGIN_CONNECTION  ANSIBLE_INVENTORY_CACHE_CONNECTION  |  | Cache connection data or path, read cache plugin documentation for specifics. |
| cache_plugin | str |  ANSIBLE_CACHE_PLUGIN  ANSIBLE_INVENTORY_CACHE_PLUGIN  |  | Cache plugin to use for the inventory's source data. |
| cache_prefix |  |  ANSIBLE_CACHE_PLUGIN_PREFIX  ANSIBLE_INVENTORY_CACHE_PLUGIN_PREFIX  |  | Prefix to use for cache plugin files/tables |
| cache_timeout | int |  ANSIBLE_CACHE_PLUGIN_TIMEOUT  ANSIBLE_INVENTORY_CACHE_TIMEOUT  |  | Cache duration in seconds |
| compose | dict |  |  | Create vars from jinja2 expressions. |
| default_ip_version |  |  |  | Choice between IPv6 and IPv4 address as the primary IP for ansible_host. |
| follow_redirects |  |  |  | Determine how redirects are followed. By default, I(follow_redirects) is set to uses urllib2 default behavior. |
| group_by | list |  |  | List of dot-sparated paths to index graphql query results (e.g. `platform.display`) The final value returned by each path is used to derive group names and then group the devices into these groups. Valid group names must be string, so indexing the dotted path should return a string (i.e. `platform.display` instead of `platform`) If value returned by the defined path is a dictionary, an attempt will first be made to access the `name` field, and then the `display` field. (i.e. `platform` would attempt to lookup `platform.name`, and if that data was not returned, it would then try `platform.display`)
 |
| group_names_raw | boolean |  | 4.6.0 | Will not add the group_by choice name to the group names |
| groups | dict |  |  | Add hosts to group based on Jinja2 conditionals. |
| keyed_groups | list |  |  | Add hosts to group based on the values of a variable. |
| leading_separator | boolean |  | 2.11 | Use in conjunction with keyed_groups. By default, a keyed group that does not have a prefix or a separator provided will have a name that starts with an underscore. This is because the default prefix is "" and the default separator is "_". Set this option to False to omit the leading underscore (or other separator) if no prefix is given. If the group name is derived from a mapping the separator is still used to concatenate the items. To not use a separator in the group name at all, set the separator for the keyed group to an empty string instead. |
| plugin |  |  |  | Setting that ensures this is a source file for the 'networktocode.nautobot' plugin. |
| query | dict |  |  | GraphQL query parameters or filters to send to Nautobot to obtain desired data |
| strict | bool |  |  | If C(yes) make invalid entries a fatal error, otherwise skip and continue. Since it is possible to use facts in the expressions they might not always be available and we ignore those errors by default. |
| timeout | int |  |  | Timeout for Nautobot requests in seconds |
| token |  |  NAUTOBOT_TOKEN  |  | Nautobot API token to be able to read against Nautobot. This may not be required depending on the Nautobot setup. |
| use_extra_vars | bool |  ANSIBLE_INVENTORY_USE_EXTRA_VARS  | 2.11 | Merge extra vars into the available variables for composition (highest precedence). |
| validate_certs | boolean |  |  | Allows connection when SSL certificates are not valid. Set to C(false) when certificates are not trusted. |


## Examples

```yaml

# inventory.yml file in YAML format
# Example command line: ansible-inventory -v --list -i inventory.yml
# Add -vvv to the command to also see the GraphQL query that gets sent in the debug output.
# Add -vvvv to the command to also see the JSON response that comes back in the debug output.

# Minimum required parameters
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000  # Can be omitted if the NAUTOBOT_URL environment variable is set
token: 1234567890123456478901234567  # Can be omitted if the NAUTOBOT_TOKEN environment variable is set

# This will send the default GraphQL query of:
# query {
#   devices {
#     name
#     primary_ip4 {
#       host
#     }
#     platform {
#       napalm_driver
#     }
#   }
#   virtual_machines {
#     name
#     primary_ip4 {
#       host
#     }
#     platform {
#       name
#     }
#   }
# }

# This module will automatically add the ansible_host key and set it equal to primary_ip4.host
# as well as the ansible_network_os key and set it to platform.napalm_driver via netutils mapping
# if the primary_ip4.host and platform.napalm_driver are present on the device in Nautobot.

# Add additional query parameters with the query key.
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
query:
  devices:
    tags: name
    serial:
    tenant: name
    location:
      name:
      contact_name:
      description:
      parent: name
  virtual_machines:
    tags: name
    tenant: name

# Add the default IP version to be used for the ansible_host
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
default_ip_version: ipv6
query:
  devices:
    tags: name
    serial:
    tenant: name
    location:
      name:
      contact_name:
      description:
      parent: name
  virtual_machines:
    tags: name
    tenant: name

# To group by use group_by key
# Specify the full path to the data you would like to use to group by.
# Ensure all paths are also included in the query.
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
query:
  devices:
    tags: name
    serial:
    tenant: name
    status: display
    location:
      name:
      contact_name:
      description:
      parent: name
  virtual_machines:
    tags: name
    tenant: name
    status: display
group_by:
  - tenant.name
  - status.display

# Filter output using any supported parameters.
# To get supported parameters check the api/docs page for devices.
# Add `filters` to any level of the dictionary and a filter will be added to the GraphQL query at that level.
# (use -vvv to see the underlying GraphQL query being sent)
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
query:
  devices:
    filters:
      name__ic: ams
    interfaces:
      filters:
        name__ic: ethernet
      name:
      ip_addresses: address

# You can filter to just devices/virtual_machines by filtering the opposite type to a name that doesn't exist.
# For example, to only get devices:
plugin: networktocode.nautobot.gql_inventory
api_endpoint: http://localhost:8000
query:
  virtual_machines:
    filters:
      name: EXCLUDE ALL

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| _list | list | list of composed dictionaries with key and value |  |

## Authors

- Network to Code (@networktocode)
- Armen Martirosyan (@armartirosyan)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
