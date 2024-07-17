# networktocode.nautobot.tag

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.tag`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.
## Synopsis

- Creates or removes tags from Nautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| color | str | 3.0.0 | Tag color |
| content_types | list |  | Tags content type(s). These match app.endpoint and the endpoint is singular. e.g. dcim.device, ipam.ipaddress (more can be found in the examples) Required if I(state=present) and the tag does not exist yet |
| description | str | 3.0.0 | Tag description |
| name | str | 3.0.0 | Tag name |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use `present` or `absent` for adding or removing. |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the [`NAUTOBOT_TOKEN`](../code_reference/environment_variables.md#nautobot_token) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the [`NAUTOBOT_URL`](../code_reference/environment_variables.md#nautobot_url) environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the [`NAUTOBOT_VALIDATE_CERTS`](../code_reference/environment_variables.md#nautobot_validate_certs) environment variable is configured. |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection local and hosts localhost

## Examples

```yaml
- name: "Test tags creation/deletion"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create tags
      networktocode.nautobot.tag:
        url: http://nautobot.local
        token: thisIsMyToken
        api_version: "1.3"
        name: "{{ item.name }}"
        description: "{{ item.description }}"
        content_types:
          - circuits.circuit
          - circuits.circuit termination
          - circuits.provider
          - circuits.provider network
          - dcim.cable
          - dcim.console port
          - dcim.console server port
          - dcim.device
          - dcim.device bay
          - dcim.device type
          - dcim.front port
          - dcim.interface
          - dcim.inventory item
          - dcim.power feed
          - dcim.power outlet
          - dcim.power panel
          - dcim.power port
          - dcim.rack
          - dcim.rack reservation
          - dcim.rear port
          - dcim.virtual chassis
          - extras.Git repository
          - extras.job
          - extras.secret
          - ipam.aggregate
          - ipam.IP address
          - ipam.prefix
          - ipam.route target
          - ipam.service
          - ipam.VLAN
          - ipam.VRF
          - tenancy.tenant
          - virtualization.cluster
          - virtualization.virtual machine
          - virtualization.VM interface
      loop:
        - { name: mgmt, description: "management" }
        - { name: tun, description: "tunnel" }
      

    - name: Delete tags
      networktocode.nautobot.tag:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "{{ item }}"
        state: absent
      loop:
        - mgmt
        - tun
```
## Return Values

| Key | Data Type | Description |
| --- | --------- | ----------- |
| tags | string | Serialized object as created/existent/updated/deleted within Nautobot<br>Returned: always |
| msg | string | Message indicating failure or info about what has been achieved<br>Returned: always |

## Authors

- Tobias Groß (@toerb)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
