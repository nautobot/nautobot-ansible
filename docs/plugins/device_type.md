# networktocode.nautobot.device_type

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.device_type`.

+++ 1.0.0
    Initial creation of Nautobot modules.

## Synopsis

- Creates, updates or removes device types from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| comments | str | 3.0.0 | Comments that may include additional information in regards to the device_type |
| custom_fields | dict | 3.0.0 | Must exist in Nautobot and in key/value format |
| is_full_depth | bool | 3.0.0 | Whether or not the device consumes both front and rear rack faces |
| manufacturer | raw | 3.0.0 | The manufacturer of the device type |
| model | raw | 3.0.0 | The model of the device type |
| part_number | str | 3.0.0 | The part number of the device type |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| subdevice_role | str | 3.0.0 | Whether the device type is parent, child, or neither |
| tags | list | 3.0.0 | Any tags that this item may need to be associated with |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| u_height | int | 3.0.0 | The height of the device type in rack units |
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
    - name: Create device type within Nautobot with only required information
      networktocode.nautobot.device_type:
        url: http://nautobot.local
        token: thisIsMyToken
        model: ws-test-3750
        manufacturer: Test Manufacturer
        state: present

    - name: Create device type within Nautobot with only required information
      networktocode.nautobot.device_type:
        url: http://nautobot.local
        token: thisIsMyToken
        model: ws-test-3750
        manufacturer: Test Manufacturer
        part_number: ws-3750g-v2
        u_height: 1
        is_full_depth: False
        subdevice_role: parent
        state: present

    - name: Delete device type within nautobot
      networktocode.nautobot.device_type:
        url: http://nautobot.local
        token: thisIsMyToken
        model: ws-test-3750
        state: absent

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| device_type | dict | Serialized object as created or already existent within Nautobot | success (when I(state=present)) |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Mikhail Yohman (@FragmentedPacket)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
