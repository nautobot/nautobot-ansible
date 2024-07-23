# networktocode.nautobot.vm_interface

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install the collection, use: 
    
    ```
    ansible-galaxy collection install networktocode.nautobot
    ```
    
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.vm_interface`.

+++ 1.0.0
    Initial creation of Nautobot modules.

## Synopsis

- Creates or removes interfaces from virtual machines in Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| custom_fields | dict | 3.0.0 | Must exist in Nautobot and in key/value format |
| description | str | 3.0.0 | The description of the interface |
| enabled | bool | 3.0.0 | Sets whether interface shows enabled or disabled |
| mac_address | str | 3.0.0 | The MAC address of the interface |
| mode | raw | 3.0.0 | The mode of the interface |
| mtu | int | 3.0.0 | The MTU of the interface |
| name | str | 3.0.0 | Name of the interface to be created |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use `present` or `absent` for adding or removing. |
| status | raw | 3.0.0 | The status of the interface. Required if _state=present_ and does not exist yet |
| tagged_vlans | raw | 3.0.0 | A list of tagged VLANS to be assigned to interface. Mode must be set to either `Tagged` or `Tagged All` |
| tags | list | 3.0.0 | Any tags that this item may need to be associated with |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the `NAUTOBOT_TOKEN` environment variable is configured. |
| untagged_vlan | raw | 3.0.0 | The untagged VLAN to be assigned to interface |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the `NAUTOBOT_URL` environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the `NAUTOBOT_VALIDATE_CERTS` environment variable is configured. |
| virtual_machine | raw | 3.0.0 | Name of the virtual machine the interface will be associated with (case-sensitive) |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection C(local) and hosts C(localhost)

## Examples

```yaml

- name: "Test Nautobot interface module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create interface within Nautobot with only required information
      networktocode.nautobot.vm_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        virtual_machine: test100
        name: GigabitEthernet1
        state: present

    - name: Delete interface within nautobot
      networktocode.nautobot.vm_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        virtual_machine: test100
        name: GigabitEthernet1
        state: absent

    - name: Create interface as a trunk port
      networktocode.nautobot.vm_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        virtual_machine: test100
        name: GigabitEthernet25
        enabled: false
        untagged_vlan:
          name: Wireless
          location: "{{ test_location['key'] }}"
        tagged_vlans:
          - name: Data
            location: "{{ test_location['key'] }}"
          - name: VoIP
            location: "{{ test_location['key'] }}"
        mtu: 1600
        mode: Tagged
        state: present

    - name: |
        Create an interface and update custom_field data point,
        setting the value to True
      networktocode.nautobot.vm_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        virtual_machine: test100
        name: GigabitEthernet26
        enabled: false
        custom_fields:
          monitored: True

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| interface | dict | Serialized object as created or already existent within Nautobot | on creation |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Benjamin Vergnaud (@bvergnaud)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
