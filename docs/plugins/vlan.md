# networktocode.nautobot.vlan

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.vlan`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.
## Synopsis

- Creates, updates or removes vlans from Nautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| description | str | 3.0.0 | The description of the vlan |
| location | raw | 3.0.0 | The single location the VLAN will be associated to If you want to associate multiple locations, use the `vlan_location` module Using this parameter will override the `api_version` option to `2.0` |
| name | str | 3.0.0 | The name of the vlan |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| role | raw | 3.0.0 | The role of the VLAN. |
| state | str |  | Use `present` or `absent` for adding or removing. |
| status | raw | 3.0.0 | The status of the vlan Required if I(state=present) and does not exist yet |
| tenant | raw | 3.0.0 | The tenant that the vlan will be assigned to |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the [`NAUTOBOT_TOKEN`](../code_reference/environment_variables.md#nautobot_token) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the [`NAUTOBOT_URL`](../code_reference/environment_variables.md#nautobot_url) environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the [`NAUTOBOT_VALIDATE_CERTS`](../code_reference/environment_variables.md#nautobot_validate_certs) environment variable is configured. |
| vid | int | 3.0.0 | The VLAN ID |
| vlan_group | raw | 3.0.0 | The VLAN group the VLAN will be associated to |

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
    - name: Create vlan within Nautobot with only required information
      networktocode.nautobot.vlan:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test VLAN
        vid: 400
        status: active
        state: present

    - name: Delete vlan within nautobot
      networktocode.nautobot.vlan:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test VLAN
        vid: 400
        status: active
        state: absent

    - name: Create vlan with all information
      networktocode.nautobot.vlan:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test VLAN
        vid: 400
        location:
          name: My Location
          parent: Parent Location
        group: Test VLAN Group
        tenant: Test Tenant
        status: Deprecated
        role: Test VLAN Role
        description: Just a test
        tags:
          - Schnozzberry
        state: present
```
## Return Values

| Key | Data Type | Description |
| --- | --------- | ----------- |
| vlan | string | Serialized object as created or already existent within Nautobot<br>Returned: always |
| msg | string | Message indicating failure or info about what has been achieved<br>Returned: always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
