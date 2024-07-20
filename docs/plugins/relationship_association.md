# networktocode.nautobot.relationship_association

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install the collection, use: 
    
    ```
    ansible-galaxy collection install networktocode.nautobot
    ```
    
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.relationship_association`.

+++ 4.0.0
    Added in 4.0.0.

## Synopsis

- Creates or removes a relationship association from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| destination_id | str |  | The UUID of the destination of the relationship |
| destination_type | str |  | The app_label.model for the destination of the relationship |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| relationship | raw |  | The Relationship UUID to add the association to |
| source_id | str |  | The UUID of the source of the relationship |
| source_type | str |  | The app_label.model for the source of the relationship |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the E(NAUTOBOT_URL) environment variable is configured. |
| validate_certs | raw |  | If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the E(NAUTOBOT_VALIDATE_CERTS) environment variable is configured. |

## Tags


## Examples

```yaml

- name: "Test relationship association creation/deletion"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create relationship association
      networktocode.nautobot.relationship_association:
        url: http://nautobot.local
        token: thisIsMyToken
        relationship: 01234567-abcd-0123-abcd-012345678901
        source_type: dcim.device
        source_id: abcdefgh-0123-abcd-0123-abcdefghijkl
        destination_type: ipam.vrf
        destination_id: 01234567-abcd-0123-abcd-123456789012

    - name: Delete relationship association
      networktocode.nautobot.relationship_association:
        url: http://nautobot.local
        token: thisIsMyToken
        relationship: 01234567-abcd-0123-abcd-012345678901
        source_type: dcim.device
        source_id: abcdefgh-0123-abcd-0123-abcdefghijkl
        destination_type: ipam.vrf
        destination_id: 01234567-abcd-0123-abcd-123456789012
        state: absent

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| msg | str | Message indicating failure or info about what has been achieved | always |
| relationship_associations | dict | Serialized object as created/existent/updated/deleted within Nautobot | always |

## Authors

- Network to Code (@networktocode)
- Joe Wesch (@joewesch)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
