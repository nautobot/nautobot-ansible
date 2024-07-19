# networktocode.nautobot.location_type

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.location_type`.

+++ 4.3.0 "Initial Modules Creation."
    Added in 4.3.0.

## Synopsis

- Creates or removes location types from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| content_types | list |  | Location Type content type(s). These match app.endpoint and the endpoint is singular. e.g. dcim.device, ipam.ipaddress (more can be found in the examples) |
| custom_fields | dict | 3.0.0 | Must exist in Nautobot and in key/value format |
| description | str |  | Location Type description |
| name | str |  | Name of the location type to be created |
| nestable | bool |  | Allow Locations of this type to be parents/children of other Locations of this same type Requires C(nautobot >= 1.5) |
| parent_location_type | raw |  | The parent location type this location type should be tied to |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the E(NAUTOBOT_URL) environment variable is configured. |
| validate_certs | raw |  | If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the E(NAUTOBOT_VALIDATE_CERTS) environment variable is configured. |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection C(local) and hosts C(localhost)

## Examples

```yaml

- name: "Test Nautobot location type module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create location type
      networktocode.nautobot.location_type:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Location Type
        state: present

    - name: Delete location type
      networktocode.nautobot.location_type:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Location Type
        state: absent

    - name: Create location type with all parameters
      networktocode.nautobot.location_type:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Nested Location Type
        description: My Nested Location Type Description
        parent:
          name: My Location Type
        nestable: false
        content_types:
          - "dcim.device"
        state: present

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| location_type | dict | Serialized object as created or already existent within Nautobot | on creation |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Joe Wesch (@joewesch)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
