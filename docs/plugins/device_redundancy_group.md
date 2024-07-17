# networktocode.nautobot.device_redundancy_group

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.device_redundancy_group`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.
## Synopsis

- Creates or removes device redundancy groups from Nautobot

## Requirements

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| description | str | 5.1.0 | The description of the device redundancy group |
| failover_strategy | str | 5.1.0 | The failover strategy of the device redundancy group |
| name | str | 5.1.0 | The name of the device redundancy group |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| secrets_group | raw | 5.1.0 | The secrets group of the device redundancy group |
| state | str |  | Use `present` or `absent` for adding or removing. |
| status | raw | 5.1.0 | The status of the device redundancy group Required if I(state=present) and the device redundancy group does not exist yet |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the [`NAUTOBOT_TOKEN`](../code_reference/environment_variables.md#nautobot_token) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the [`NAUTOBOT_URL`](../code_reference/environment_variables.md#nautobot_url) environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the [`NAUTOBOT_VALIDATE_CERTS`](../code_reference/environment_variables.md#nautobot_validate_certs) environment variable is configured. |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection local and hosts localhost

## Examples

```yaml
- name: "Test Nautobot device_redundancy_group module"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create device redundancy group within Nautobot with only required information
      networktocode.nautobot.device_redundancy_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Redundancy Group
        status: Active
        state: present
    
    - name: Create device redundancy group within Nautobot with all information
      networktocode.nautobot.device_redundancy_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Redundancy Group
        status: Active
        description: My Description
        failover_strategy: active-active
        secrets_group: "{{ my_secrets_group['key'] }}"
        tags:
          - My Tag
        custom_fields:
          my_field: my_value
        state: present
      vars:
        my_secrets_group: "{{ lookup('networktocode.nautobot.lookup', 'secrets-groups', api_endpoint=nautobot_url, token=nautobot_token, api_filter='name=\"My Secrets Group\"') }}"
    
    - name: Delete device redundancy group within nautobot
      networktocode.nautobot.device_redundancy_group:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Redundancy Group
        state: absent
```
## Return Values

| Key | Data Type | Description |
| --- | --------- | ----------- |
| device_redundancy_group | string | Serialized object as created or already existent within Nautobot<br>Returned: always |
| msg | string | Message indicating failure or info about what has been achieved<br>Returned: always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
