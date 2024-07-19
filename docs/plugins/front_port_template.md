# networktocode.nautobot.front_port_template

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.front_port_template`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.

## Synopsis

- Creates, updates or removes front port templates from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| device_type | raw | 3.0.0 | The device type the front port template is attached to |
| name | str | 3.0.0 | The name of the front port template |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| rear_port_template | raw | 3.0.0 | The rear_port_template the front port template is attached to |
| rear_port_template_position | int | 3.0.0 | The position of the rear port template this front port template is connected to |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| type | str | 3.0.0 | The type of the front port template |
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
    - name: Create front port template within Nautobot with only required information
      networktocode.nautobot.front_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Front Port Template
        device_type: Test Device Type
        type: bnc
        rear_port_template: Test Rear Port Template
        state: present

    - name: Update front port template with other fields
      networktocode.nautobot.front_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
        name: Test Front Port Template
        device_type: Test Device Type
        type: bnc
        rear_port_template: Test Rear Port Template
        rear_port_template_position: 5
        state: present

    - name: Delete front port template within nautobot
      networktocode.nautobot.front_port_template:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Front Port Template
        device_type: Test Device Type
        type: bnc
        rear_port_template: Test Rear Port Template
        state: absent

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| front_port_template | dict | Serialized object as created or already existent within Nautobot | success (when I(state=present)) |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
