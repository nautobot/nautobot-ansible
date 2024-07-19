# networktocode.nautobot.controller

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.controller`.

+++ 5.3.0 "Initial Modules Creation."
    Added in 5.3.0.

## Synopsis

- {'Creates, updates or removes controllers from Nautobot, related page': 'https://docs.nautobot.com/projects/core/en/stable/user-guide/core-data-model/dcim/controller/'}

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| controller_device | string | 5.3.0 | Device that runs the controller software |
| controller_device_redundancy_group | string | 5.3.0 | Related device redundancy group the device will be assigned to |
| custom_fields | dict | 3.0.0 | Must exist in Nautobot and in key/value format |
| external_integration | string | 5.3.0 | External connection for the controller, such as Meraki Cloud URL |
| location | raw | 5.3.0 | Required if I(state=present) and the device does not exist yet |
| name | str | 5.3.0 | The name of the controller |
| platform | raw | 5.3.0 | The platform of the device |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| role | raw | 5.3.0 | Required if I(state=present) and the device does not exist yet |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| status | raw | 5.3.0 | The status of the device Required if I(state=present) and the device does not exist yet |
| tags | list | 3.0.0 | Any tags that this item may need to be associated with |
| tenant | raw | 5.3.0 | The tenant that the device will be assigned to |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the E(NAUTOBOT_URL) environment variable is configured. |
| validate_certs | raw |  | If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the E(NAUTOBOT_VALIDATE_CERTS) environment variable is configured. |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection C(local) and hosts C(localhost)

## Examples

```yaml

- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create device within Nautobot with only required information
      networktocode.nautobot.controller:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "test_controller_2"
        location: My Location
        status: "Active"
        state: present

    - name: "CREATE THE SECOND CONTROLLER"
      networktocode.nautobot.controller:
        name: "test_controller_3"
        url: http://nautobot.local
        token: thisIsMyToken
        status: "Active"
        location: "Cisco"
        external_integration: "Cisco Catalyst SD-WAN"
        role: "Administrative"
        platform: "Cisco IOS"
        tenant: "Nautobot Baseball Stadiums"
        controller_device_redundancy_group: "controller_test"

    - name: Delete device within nautobot
      networktocode.nautobot.controller:
        url: http://nautobot.local
        token: thisIsMyToken
        name: test_controller_3
        state: absent


```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| device | dict | Serialized object as created or already existent within Nautobot | success (when I(state=present)) |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Josh VanDeraa (@jvanderaa)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
