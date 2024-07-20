# networktocode.nautobot.lookup

!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install the collection, use: 
    
    ```
    ansible-galaxy collection install networktocode.nautobot
    ```
    
    You need further requirements to be able to use this module, see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `networktocode.nautobot.lookup`.

## Synopsis

- Queries Nautobot via its API to return virtually any information capable of being held in Nautobot.

## Requirements

The below requirements are needed on the host that executes this module.

- pynautobot

## Parameters

| Parameter | Data Type | Environment Variable | Version Added | Comments |
| --------- | --------- | -------------------- | ------------- | -------- |
| _terms |  |  |  | The Nautobot object type to query |
| api_endpoint |  |  NAUTOBOT_URL  |  | The URL to the Nautobot instance to query |
| api_filter |  |  |  | The api_filter to use. |
| api_version |  |  | 4.1.0 | The Nautobot Rest API version to use. |
| num_retries |  |  |  | Number of retries This will only affect HTTP codes 429, 500, 502, 503, and 504. |
| plugin |  |  |  | The Nautobot plugin to query |
| raw_data |  |  |  | Whether to return raw API data with the lookup/query or whether to return a key/value dict |
| token |  |  NAUTOBOT_TOKEN  |  | The API token created through Nautobot This may not be required depending on the Nautobot setup. |
| validate_certs |  |  |  | Whether or not to validate SSL of the Nautobot instance |


## Examples

```yaml

tasks:
  # query a list of devices
  - name: Obtain list of devices from Nautobot
    debug:
      msg: >
        "Device {{ item.value.display_name }} (ID: {{ item.key }}) was
         manufactured by {{ item.value.device_type.manufacturer.name }}"
    loop: "{{ query('networktocode.nautobot.lookup', 'devices',
                    api_endpoint='http://localhost/',
                    api_version='2.0',
                    token='<redacted>') }}"

# This example uses an API Filter
tasks:
  # query a list of devices
  - name: Obtain list of devices from Nautobot
    debug:
      msg: >
        "Device {{ item.value.display_name }} (ID: {{ item.key }}) was
         manufactured by {{ item.value.device_type.manufacturer.name }}"
    loop: "{{ query('networktocode.nautobot.lookup', 'devices',
                    api_endpoint='http://localhost/',
                    api_version='2.0',
                    api_filter='role=management tags=Dell',
                    token='<redacted>') }}"

# This example uses an API Filter with Depth set to get additional details from the lookup
tasks:
  # query a list of devices, getting API Depth of 1 to get additional details
  # Note the space and the use of depth. Note the location_name is set to the namae of the location
    - name: "Obtain Location Information from Nautobot and print some facts."
      ansible.builtin.debug:
        msg: >
          "Location {{ item.value.name }} is  {{ item.value['status']['name'] }} and has {{ item.value.prefix_count }} Prefixes and {{ item.value.vlan_count }} VLANs."
      loop: "{{ query('networktocode.nautobot.lookup', 'locations',
        url=NAUTOBOT_URL,
        token=NAUTOBOT_TOKEN,
        api_filter='name=' + location_name + ' depth=1',
        ) }}"


# Fetch bgp sessions for R1-device
tasks:
  - name: "Obtain bgp sessions for R1-Device"
    debug:
      msg: "{{ query('networktocode.nautobot.lookup', 'bgp_sessions',
                     api_filter='device=R1-Device',
                     api_endpoint='http://localhost/',
                     api_version='2.0',
                     token='<redacted>',
                     plugin='mycustomstuff') }}"

```

## Return Values

| Key | Data Type | Description | Returned | 
| --- | --------- | ----------- | -------- |
| _list | list | list of composed dictionaries with key and value |  |

## Authors

- Chris Mills (@cpmills1975)

## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)
