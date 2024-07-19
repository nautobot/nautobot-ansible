# networktocode.nautobot.tenant

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.tenant`.

+++ 1.0.0
    Initial creation of Nautobot modules.

## Synopsis

- Creates or removes tenants from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| comments | str | 3.0.0 | Comments for the tenant. This can be markdown syntax |
| custom_fields | dict | 3.0.0 | Must exist in Nautobot and in key/value format |
| description | str | 3.0.0 | The description of the tenant |
| name | str | 3.0.0 | Name of the tenant to be created |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| tags | list | 3.0.0 | Any tags that this item may need to be associated with |
| tenant_group | raw | 3.0.0 | Tenant group this tenant should be in |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the E(NAUTOBOT_URL) environment variable is configured. |
| validate_certs | raw |  | If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the E(NAUTOBOT_VALIDATE_CERTS) environment variable is configured. |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection C(local) and hosts C(localhost)

## Examples

```yaml

- name: "Test Nautobot module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create tenant within Nautobot with only required information
      networktocode.nautobot.tenant:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Tenant ABC
        state: present

    - name: Delete tenant within nautobot
      networktocode.nautobot.tenant:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Tenant ABC
        state: absent

    - name: Create tenant with all parameters
      networktocode.nautobot.tenant:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Tenant ABC
        tenant_group: Very Special Tenants
        description: ABC Incorporated
        comments: '### This tenant is super cool'
        tags:
          - tagA
          - tagB
          - tagC
        state: present

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| msg | str | Message indicating failure or info about what has been achieved | always |
| tenant | dict | Serialized object as created or already existent within Nautobot | on creation |

## Authors

- Amy Liebowitz (@amylieb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
