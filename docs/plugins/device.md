# networktocode.nautobot.device

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.device`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.
## Synopsis

- Creates, updates or removes devices from Nautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| asset_tag | str | 3.0.0 | Asset tag that is associated to the device |
| cluster | raw | 3.0.0 | Cluster that the device will be assigned to |
| comments | str | 3.0.0 | Comments that may include additional information in regards to the device |
| device_redundancy_group | raw | 5.1.0 | Device redundancy group the device will be assigned to |
| device_redundancy_group_priority | int | 5.1.0 | Priority in the assigned device redundancy group |
| device_type | raw | 3.0.0 | Required if I(state=present) and the device does not exist yet |
| face | str | 3.0.0 | Required if I(rack) is defined |
| local_config_context_data | dict | 3.0.0 | Arbitrary JSON data to define the devices configuration variables. |
| location | raw | 3.0.0 | Required if I(state=present) and the device does not exist yet |
| name | str | 3.0.0 | The name of the device |
| platform | raw | 3.0.0 | The platform of the device |
| position | int | 3.0.0 | The position of the device in the rack defined above |
| primary_ip4 | raw | 3.0.0 | Primary IPv4 address assigned to the device |
| primary_ip6 | raw | 3.0.0 | Primary IPv6 address assigned to the device |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| rack | raw | 3.0.0 | The name of the rack to assign the device to |
| role | raw | 3.0.0 | Required if I(state=present) and the device does not exist yet |
| serial | str | 3.0.0 | Serial number of the device |
| state | str |  | Use `present` or `absent` for adding or removing. |
| status | raw | 3.0.0 | The status of the device Required if I(state=present) and the device does not exist yet |
| tenant | raw | 3.0.0 | The tenant that the device will be assigned to |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the [`NAUTOBOT_TOKEN`](../code_reference/environment_variables.md#nautobot_token) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the [`NAUTOBOT_URL`](../code_reference/environment_variables.md#nautobot_url) environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the [`NAUTOBOT_VALIDATE_CERTS`](../code_reference/environment_variables.md#nautobot_validate_certs) environment variable is configured. |
| vc_position | int | 3.0.0 | Position in the assigned virtual chassis |
| vc_priority | int | 3.0.0 | Priority in the assigned virtual chassis |
| virtual_chassis | raw | 3.0.0 | Virtual chassis the device will be assigned to |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection local and hosts localhost

## Examples

```yaml
- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create device within Nautobot with only required information
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Device
        device_type: C9410R
        role: Core Switch
        location: My Location
        status: active
        state: present

    - name: Create device within Nautobot with empty string name to generate UUID
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        name: ""
        device_type: C9410R
        role: Core Switch
        location:
          name: My Location
          parent: Parent Location
        status: active
        state: present

    - name: Delete device within nautobot
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Device
        state: absent

    - name: Create device with tags
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Another Test Device
        device_type: C9410R
        role: Core Switch
        location:
          name: My Location
          parent: Parent Location
        status: active
        local_config_context_data:
          bgp: "65000"
        tags:
          - Schnozzberry
        state: present

    - name: Update the rack and position of an existing device
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Device
        rack: Test Rack
        position: 10
        face: Front
        state: present
```
## Return Values

| Key | Data Type | Description |
| --- | --------- | ----------- |
| device | string | Serialized object as created or already existent within Nautobot<br>Returned: always |
| msg | string | Message indicating failure or info about what has been achieved<br>Returned: always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
