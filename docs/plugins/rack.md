# networktocode.nautobot.rack

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install the collection, use: 
    
    ```
    ansible-galaxy collection install networktocode.nautobot
    ```
    
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.rack`.

+++ 1.0.0
    Initial creation of Nautobot modules.

## Synopsis

- Creates, updates or removes racks from Nautobot.

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| asset_tag | str | 3.0.0 | Asset tag that is associated to the rack. |
| comments | str | 3.0.0 | Comments that may include additional information in regards to the rack. |
| custom_fields | dict | 3.0.0 | Must exist in Nautobot and in key/value format |
| desc_units | bool | 3.0.0 | Rack units will be numbered top-to-bottom. |
| facility_id | str | 3.0.0 | The unique rack ID assigned by the facility. |
| location | raw | 3.0.0 | Required if _state=present_ and the rack does not exist yet. |
| name | str | 3.0.0 | The name of the rack. |
| outer_depth | int | 3.0.0 | The outer depth of the rack. |
| outer_unit | str | 3.0.0 | Whether the rack unit is in Millimeters or Inches and is _required_ if outer_width/outer_depth is specified. |
| outer_width | int | 3.0.0 | The outer width of the rack. |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| rack_group | raw | 3.0.0 | The rack group the rack will be associated to. |
| role | raw | 3.0.0 | The rack role the rack will be associated to. |
| serial | str | 3.0.0 | Serial number of the rack. |
| state | str |  | Use `present` or `absent` for adding or removing. |
| status | raw | 3.0.0 | The status of the rack Required if _state=present_ and does not exist yet. |
| tags | list | 3.0.0 | Any tags that this item may need to be associated with |
| tenant | raw | 3.0.0 | The tenant that the device will be assigned to. |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the `NAUTOBOT_TOKEN` environment variable is configured. |
| type | str | 3.0.0 | The type of rack. |
| u_height | int | 3.0.0 | The height of the rack in rack units. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the `NAUTOBOT_URL` environment variable is configured. |
| validate_certs | raw |  | If `no`, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the `NAUTOBOT_VALIDATE_CERTS` environment variable is configured. |
| width | int | 3.0.0 | The rail-to-rail width. |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list.
    * This should be ran with connection C(local) and hosts C(localhost).
    * The module supports C(check_mode).

## Examples

```yaml

- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create rack within Nautobot with only required information
      networktocode.nautobot.rack:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test rack
        location:
          name: My Location
          parent: Parent Location
        status: active
        state: present

    - name: Delete rack within nautobot
      networktocode.nautobot.rack:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test Rack
        state: absent

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| msg | str | Message indicating failure or info about what has been achieved. | always |
| rack | dict | Serialized object as created or already existent within Nautobot. | success (when I(state=present)) |

## Authors

- NMikhail Yohman (@FragmentedPacket)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
