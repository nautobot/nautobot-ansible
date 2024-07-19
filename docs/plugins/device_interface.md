# networktocode.nautobot.device_interface

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.device_interface`.

+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.

## Synopsis

- Creates or removes interfaces from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| bridge | raw | 4.5.0 | Interface that will be the bridge of the interface being created |
| custom_fields | dict | 3.0.0 | Must exist in Nautobot and in key/value format |
| description | str | 3.0.0 | The description of the interface |
| device | raw | 3.0.0 | Name of the device the interface will be associated with (case-sensitive) |
| enabled | bool | 3.0.0 | Sets whether interface shows enabled or disabled |
| label | str | 3.0.0 | Physical label of the interface |
| lag | raw | 3.0.0 | Parent LAG interface will be a member of |
| mac_address | str | 3.0.0 | The MAC address of the interface |
| mgmt_only | bool | 3.0.0 | This interface is used only for out-of-band management |
| mode | raw | 3.0.0 | The mode of the interface |
| mtu | int | 3.0.0 | The MTU of the interface |
| name | str | 3.0.0 | Name of the interface to be created |
| parent_interface | raw | 4.5.0 | Interface that will be the parent of the interface being created |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| status | raw | 4.5.0 | The status of the interface Required if I(state=present) and the interface does not exist yet |
| tagged_vlans | raw | 3.0.0 | A list of tagged VLANS to be assigned to interface. Mode must be set to either C(Tagged) or C(Tagged All) |
| tags | list | 3.0.0 | Any tags that this item may need to be associated with |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| type | str | 3.0.0 | Form factor of the interface:
ex. 1000Base-T (1GE), Virtual, 10GBASE-T (10GE)
This has to be specified exactly as what is found within UI
 |
| untagged_vlan | raw | 3.0.0 | The untagged VLAN to be assigned to interface |
| update_vc_child | bool | 3.0.0 | Use when master device is specified for C(device) and the specified interface exists on a child device
and needs updated
 |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the E(NAUTOBOT_URL) environment variable is configured. |
| validate_certs | raw |  | If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the E(NAUTOBOT_VALIDATE_CERTS) environment variable is configured. |

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
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: GigabitEthernet1
        state: present
    - name: Delete interface within nautobot
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: GigabitEthernet1
        state: absent
    - name: Create LAG with several specified options
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: port-channel1
        type: Link Aggregation Group (LAG)
        mtu: 1600
        mgmt_only: false
        mode: Access
        state: present
    - name: Create interface and assign it to parent LAG
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: GigabitEthernet1
        enabled: false
        type: 1000Base-t (1GE)
        lag:
          name: port-channel1
        mtu: 1600
        mgmt_only: false
        mode: Access
        state: present
    - name: Create interface as a trunk port
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: GigabitEthernet25
        enabled: false
        type: 1000Base-t (1GE)
        untagged_vlan:
          name: Wireless
          location: "{{ location['key'] }}"
        tagged_vlans:
          - name: Data
            location: "{{ location['key'] }}"
          - name: VoIP
            location: "{{ location['key'] }}"
        mtu: 1600
        mgmt_only: true
        mode: Tagged
        state: present
    - name: Update interface on child device on virtual chassis
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: GigabitEthernet2/0/1
        enabled: false
        update_vc_child: True
    - name: |
        Create an interface and update custom_field data point,
        setting the value to True
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: GigabitEthernet1/1/1
        enabled: false
        custom_fields:
          monitored: True
    - name: Create child interface
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: GigabitEthernet1/1/1
        type: Virtual
        parent_interface:
          name: GigabitEthernet1/1
    - name: Create bridge interface
      networktocode.nautobot.device_interface:
        url: http://nautobot.local
        token: thisIsMyToken
        device: test100
        name: Bridge1
        bridge:
          name: GigabitEthernet1/1

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| interface | dict | Serialized object as created or already existent within Nautobot | on creation |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Mikhail Yohman (@FragmentedPacket)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
