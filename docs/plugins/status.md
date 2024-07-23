# networktocode.nautobot.status

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install the collection, use: 
    
    ```
    ansible-galaxy collection install networktocode.nautobot
    ```
    
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.status`.

+++ 1.0.0
    Initial creation of Nautobot modules.

## Synopsis

- Creates or removes status from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| color | str | 3.0.0 | Status color |
| content_types | list | 3.0.0 | Status content type(s). These match app.endpoint and the endpoint is singular. e.g. dcim.device, ipam.ipaddress (more can be found in the examples) |
| description | str | 3.0.0 | The description for the status |
| name | str | 3.0.0 | Status name |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use `present` or `absent` for adding or removing. |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the `NAUTOBOT_TOKEN` environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the `NAUTOBOT_URL` environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the `NAUTOBOT_VALIDATE_CERTS` environment variable is configured. |

## Tags

!!! note "Note"
    * Status should be defined as a YAML list

## Examples

```yaml

- name: "Test status creation/deletion"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create status
      networktocode.nautobot.status:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "ansible_status"
        description: "Status if provisioned by Ansible"
        content_types:
          - dcim.device
          - dcim.cable
          - dcim.powerfeed
          - dcim.rack
          - circuits.circuit
          - virtualization.virtualmachine
          - ipam.prefix
          - ipam.ipaddress
          - ipam.vlan
        color: 01bea3

    - name: Delete status
      networktocode.nautobot.status:
        url: http://nautobot.local
        token: thisIsMyToken
        name: "ansible_status"
        state: absent

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| msg | str | Message indicating failure or info about what has been achieved | always |
| statuses | dict | Serialized object as created/existent/updated/deleted within Nautobot | always |

## Authors

- Network to Code (@networktocode)
- Mikhail Yohman (@fragmentedpacket)
- Josh VanDeraa (@jvanaderaa)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
