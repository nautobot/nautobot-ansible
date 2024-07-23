# networktocode.nautobot.provider

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install the collection, use: 
    
    ```
    ansible-galaxy collection install networktocode.nautobot
    ```
    
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.provider`.

+++ 1.0.0
    Initial creation of Nautobot modules.

## Synopsis

- Creates, updates or removes providers from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| account | str | 3.0.0 | The account number of the provider |
| admin_contact | str | 3.0.0 | The admin contact of the provider |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| asn | int | 3.0.0 | The provider ASN |
| comments | str | 3.0.0 | Comments related to the provider |
| custom_fields | dict | 3.0.0 | Must exist in Nautobot and in key/value format |
| name | str | 3.0.0 | The name of the provider |
| noc_contact | str | 3.0.0 | The NOC contact of the provider |
| portal_url | str | 3.0.0 | The URL of the provider |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use `present` or `absent` for adding or removing. |
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

- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create provider within Nautobot with only required information
      networktocode.nautobot.provider:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Provider
        state: present

    - name: Update provider with other fields
      networktocode.nautobot.provider:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Provider
        asn: 65001
        account: 200129104
        portal_url: http://provider.net
        noc_contact: noc@provider.net
        admin_contact: admin@provider.net
        comments: "BAD PROVIDER"
        state: present

    - name: Delete provider within nautobot
      networktocode.nautobot.provider:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Provider
        state: absent

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| msg | str | Message indicating failure or info about what has been achieved | always |
| provider | dict | Serialized object as created or already existent within Nautobot | success (when I(state=present)) |

## Authors

- Mikhail Yohman (@FragmentedPacket)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
