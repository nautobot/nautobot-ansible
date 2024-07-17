# networktocode.nautobot.rear_port

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.rear_port`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.
## Synopsis

- Creates, updates or removes rear ports from Nautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| description | str | 3.0.0 | Description of the rear port |
| device | raw | 3.0.0 | The device the rear port is attached to |
| name | str | 3.0.0 | The name of the rear port |
| positions | int | 3.0.0 | The number of front ports which may be mapped to each rear port |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use `present` or `absent` for adding or removing. |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the [`NAUTOBOT_TOKEN`](../code_reference/environment_variables.md#nautobot_token) environment variable is configured. |
| type | str | 3.0.0 | The type of the rear port |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the [`NAUTOBOT_URL`](../code_reference/environment_variables.md#nautobot_url) environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the [`NAUTOBOT_VALIDATE_CERTS`](../code_reference/environment_variables.md#nautobot_validate_certs) environment variable is configured. |

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
    - name: Create rear port within Nautobot with only required information
      networktocode.nautobot.rear_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rear Port
        device: Test Device
        type: bnc
        state: present

    - name: Update rear port with other fields
      networktocode.nautobot.rear_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rear Port
        device: Test Device
        type: bnc
        positions: 5
        description: rear port description
        state: present

    - name: Delete rear port within nautobot
      networktocode.nautobot.rear_port:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rear Port
        device: Test Device
        type: bnc
        state: absent
```
## Return Values

| Key | Data Type | Description |
| --- | --------- | ----------- |
| rear_port | string | Serialized object as created or already existent within Nautobot<br>Returned: always |
| msg | string | Message indicating failure or info about what has been achieved<br>Returned: always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
