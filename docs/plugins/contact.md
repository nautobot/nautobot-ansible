# networktocode.nautobot.contact

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.contact`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.
## Synopsis

- Creates or removes contacts from Nautobot

## Requirements

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| address | str |  | The address of the contact |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| comments | str |  | Comments about the contact |
| email | str |  | The email of the contact |
| name | str |  | The name of the contact |
| phone | str |  | The phone number of the contact |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use `present` or `absent` for adding or removing. |
| teams | list |  | The teams the contact is associated with |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the [`NAUTOBOT_TOKEN`](../code_reference/environment_variables.md#nautobot_token) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the [`NAUTOBOT_URL`](../code_reference/environment_variables.md#nautobot_url) environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the [`NAUTOBOT_VALIDATE_CERTS`](../code_reference/environment_variables.md#nautobot_validate_certs) environment variable is configured. |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection local and hosts localhost

## Examples

```yaml
---
- name: Create a contact
  networktocode.nautobot.contact:
    url: http://nautobot.local
    token: thisIsMyToken
    name: My Contact
    phone: 123-456-7890
    email: user@example.com
    address: 1234 Main St
    teams:
      - name: team1
      - name: team2
    comments: My Comments
    tags:
      - tag1
      - tag2
    custom_fields:
      my_custom_field: my_value
    state: present

- name: Delete a contact
  networktocode.nautobot.contact:
    url: http://nautobot.local
    token: thisIsMyToken
    name: My Contact
    state: absent
```
## Return Values

| Key | Data Type | Description |
| --- | --------- | ----------- |
| contact | string | Serialized object as created or already existent within Nautobot<br>Returned: always |
| msg | string | Message indicating failure or info about what has been achieved<br>Returned: always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
