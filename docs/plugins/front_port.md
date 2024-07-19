# networktocode.nautobot.front_port

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.front_port`.

+++ 1.0.0
    Initial creation of Nautobot modules.

## Synopsis

- Creates, updates or removes front ports from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| description | str | 3.0.0 | Description of the front port |
| device | raw | 3.0.0 | The device the front port is attached to |
| name | str | 3.0.0 | The name of the front port |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| rear_port | raw | 3.0.0 | The rear_port the front port is attached to |
| rear_port_position | int | 3.0.0 | The position of the rear port this front port is connected to |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| tags | list | 3.0.0 | Any tags that this item may need to be associated with |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| type | str | 3.0.0 | The type of the front port |
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
    - name: Create front port within Nautobot with only required information
      networktocode.nautobot.front_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Front Port
        device: Test Device
        type: bnc
        rear_port: Test Rear Port
        state: present

    - name: Update front port with other fields
      networktocode.nautobot.front_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Front Port
        device: Test Device
        type: bnc
        rear_port: Test Rear Port
        rear_port_position: 5
        description: front port description
        state: present

    - name: Delete front port within nautobot
      networktocode.nautobot.front_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Front Port
        device: Test Device
        type: bnc
        rear_port: Test Rear Port
        state: absent

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| front_port | dict | Serialized object as created or already existent within Nautobot | success (when I(state=present)) |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
