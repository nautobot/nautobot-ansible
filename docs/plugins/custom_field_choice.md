# networktocode.nautobot.custom_field_choice

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.custom_field_choice`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.
## Synopsis

- Creates or removes custom field choices from Nautobot

## Requirements

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| custom_field | raw | 5.1.0 | Custom field this choice belongs to |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use `present` or `absent` for adding or removing. |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the [`NAUTOBOT_TOKEN`](../code_reference/environment_variables.md#nautobot_token) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the [`NAUTOBOT_URL`](../code_reference/environment_variables.md#nautobot_url) environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the [`NAUTOBOT_VALIDATE_CERTS`](../code_reference/environment_variables.md#nautobot_validate_certs) environment variable is configured. |
| value | str | 5.1.0 | Value of this choice |
| weight | int | 5.1.0 | Weight of this choice |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection local and hosts localhost

## Examples

```yaml
---
- name: Create a custom field choice
  networktocode.nautobot.custom_field_choice:
    url: http://nautobot.local
    token: thisIsMyToken
    value: "Choice 1"
    weight: 100
    custom_field: "Custom Field 1"
    state: present
```
## Return Values

| Key | Data Type | Description |
| --- | --------- | ----------- |
| custom_field_choice | string | Serialized object as created or already existent within Nautobot<br>Returned: always |
| msg | string | Message indicating failure or info about what has been achieved<br>Returned: always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
