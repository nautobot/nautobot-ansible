# networktocode.nautobot.device_redundancy_group

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install the collection, use: 
    
    ```
    ansible-galaxy collection install networktocode.nautobot
    ```
    
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.device_redundancy_group`.

+++ 5.1.0
    Added in 5.1.0.

## Synopsis

- Creates or removes device redundancy groups from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| custom_fields | dict | 3.0.0 | Must exist in Nautobot and in key/value format |
| description | str | 5.1.0 | The description of the device redundancy group |
| failover_strategy | str | 5.1.0 | The failover strategy of the device redundancy group |
| name | str | 5.1.0 | The name of the device redundancy group |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| secrets_group | raw | 5.1.0 | The secrets group of the device redundancy group |
| state | str |  | Use `present` or `absent` for adding or removing. |
| status | raw | 5.1.0 | The status of the device redundancy group Required if _state=present_ and the device redundancy group does not exist yet |
| tags | list | 3.0.0 | Any tags that this item may need to be associated with |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the `NAUTOBOT_TOKEN` environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the `NAUTOBOT_URL` environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the `NAUTOBOT_VALIDATE_CERTS` environment variable is configured. |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection C(local) and hosts C(localhost)

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

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| device_redundancy_group | dict | Serialized object as created or already existent within Nautobot | success (when I(state=present)) |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Joe Wesch (@joewesch)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
