# networktocode.nautobot.location

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install the collection, use: 
    
    ```
    ansible-galaxy collection install networktocode.nautobot
    ```
    
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.location`.

+++ 4.3.0
    Added in 4.3.0.

## Synopsis

- Creates or removes locations from Nautobot

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Version Added | Comments |
| --------- | --------- | ------------- | -------- |
| api_version | str | 4.1.0 | API Version Nautobot REST API |
| asn | int | 5.1.0 | The ASN associated with the location |
| comments | str | 5.1.0 | Comments for the location. This can be markdown syntax |
| contact_email | str | 5.1.0 | Contact email for location |
| contact_name | str | 5.1.0 | Name of contact for location |
| contact_phone | str | 5.1.0 | Contact phone number for location |
| custom_fields | dict | 3.0.0 | Must exist in Nautobot and in key/value format |
| description | str |  | Location description |
| facility | str | 5.1.0 | Data center provider or facility, ex. Equinix NY7 |
| id | str |  | Primary Key of the location, used to delete the location. Because of hierarchical nature of locations and name being not unique across locations, it's a user responsibility to query location and pass its id(PK) to the task to delete the location. |
| latitude | str | 5.1.0 | Latitude in decimal format |
| location_type | raw |  | The type of location Required if I(state=present) and does not exist yet |
| longitude | str | 5.1.0 | Longitude in decimal format |
| name | str |  | Name of the location to be created |
| parent_location | raw |  | The parent location this location should be tied to |
| physical_address | str | 5.1.0 | Physical address of location |
| query_params | list | 3.0.0 | This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined in plugins/module_utils/utils.py and provides control to users on what may make an object unique in their environment. |
| shipping_address | str | 5.1.0 | Shipping address of location |
| state | str |  | Use C(present) or C(absent) for adding or removing. |
| status | raw |  | Status of the location Required if I(state=present) and does not exist yet |
| tags | list | 3.0.0 | Any tags that this item may need to be associated with |
| tenant | raw | 5.1.0 | The tenant the location will be assigned to |
| time_zone | str | 5.1.0 | Timezone associated with the location, ex. America/Denver |
| token | str |  | The token created within Nautobot to authorize API access Can be omitted if the E(NAUTOBOT_TOKEN) environment variable is configured. |
| url | str |  | The URL of the Nautobot instance resolvable by the Ansible host (for example: http://nautobot.example.com:8000) Can be omitted if the E(NAUTOBOT_URL) environment variable is configured. |
| validate_certs | raw |  | If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates. Can be omitted if the E(NAUTOBOT_VALIDATE_CERTS) environment variable is configured. |

## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection C(local) and hosts C(localhost)

## Examples

```yaml

- name: "Test Nautobot location module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create location
      networktocode.nautobot.location:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Location
        status: Active
        location_type:
          name: My Location Type
        state: present

    - name: Delete location
      networktocode.nautobot.location:
        url: http://nautobot.local
        token: thisIsMyToken
        id: "{{ location_to_delete['key'] }}"
        state: absent
      vars:
        location_to_delete: "{{ lookup('networktocode.nautobot.lookup', 'locations', api_endpoint=nautobot_url, token=nautobot_token, api_filter='name=\"My Location\" parent_location=\"Location Parent\" location_type=\"Main Type\"') }}"

    - name: Create location with all parameters
      networktocode.nautobot.location:
        url: http://nautobot.local
        token: thisIsMyToken
        name: My Nested Location
        status: Active
        location_type:
          name: My Location Type
        description: My Nested Location Description
        tenant: Test Tenant
        facility: EquinoxCA7
        asn: "65001"
        time_zone: America/Los Angeles
        physical_address: Hollywood, CA, 90210
        shipping_address: Hollywood, CA, 90210
        latitude: "10.100000"
        longitude: "12.200000"
        contact_name: Jenny
        contact_phone: 867-5309
        contact_email: jenny@example.com
        comments: "**This** is a `markdown` comment"
        parent: My Location
        state: present

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| location | dict | Serialized object as created or already existent within Nautobot | on creation |
| msg | str | Message indicating failure or info about what has been achieved | always |

## Authors

- Joe Wesch (@joewesch)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
