# networktocode.nautobot.inventory_item

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.inventory_item`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.

## Synopsis

- Creates or removes inventory items from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| asset_tag | str | 3.0.0 | The asset tag of the inventory item |
| custom_fields | dict | 3.0.0 | Must exist in Nautobot and in key/value format |
| description | str | 3.0.0 | The description of the inventory item |
| device | raw | 3.0.0 | Name of the device the inventory item belongs to |
| discovered | bool | 3.0.0 | Set the discovery flag for the inventory item |
| manufacturer | raw | 3.0.0 | The manufacturer of the inventory item |
| name | str | 3.0.0 | Name of the inventory item to be created |
| part_id | str | 3.0.0 | The part ID of the inventory item |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| serial | str | 3.0.0 | The serial number of the inventory item |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| tags | list | 3.0.0 | Any tags that this item may need to be associated with |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the E(NAUTOBOT_URL) environment variable is configured. |
| validate_certs | raw |  | If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the E(NAUTOBOT_VALIDATE_CERTS) environment variable is configured. |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection C(local) and hosts C(localhost)

## Examples

```yaml

- name: "Test Nautobot inventory_item module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create inventory item within Nautobot with only required information
      networktocode.nautobot.inventory_item:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: "10G-SFP+"
        state: present

    - name: Update inventory item
      networktocode.nautobot.inventory_item:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: "10G-SFP+"
        manufacturer: "Cisco"
        part_id: "10G-SFP+"
        serial: "1234"
        asset_tag: "1234"
        description: "New SFP"
        state: present

    - name: Delete inventory item within nautobot
      networktocode.nautobot.inventory_item:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: "10G-SFP+"
        state: absent

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| inventory_item | dict | Serialized object as created or already existent within Nautobot | on creation |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Mikhail Yohman (@FragmentedPacket)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
