# Advanced Usage

## Using query_params Module Argument

There will be times when you want to override the builtin **ALLOWED_QUERY_PARAMS** to provide a unique search of an object.

To make this possible, every module accepts the `query_params` parameter. This parameter allows you to specify a list of strings for the module parameter you want to use to search for the object.

The majority of the examples where there would be some duplicate objects have mostly been fixed up within the Nautobot project. Nautobot has obviated the need for query parameters in most use cases. This section remains as a reference, should future scenarios require this capability.

```yaml
---
# Corresponding to the docs/user_guide/advanced.md examples
- name: "EXAMPLE PLAY: Add IP Address to Nautobot"
  hosts: localhost
  connection: local
  gather_facts: no
  vars:
    nautobot_url: "{{ lookup('ansible.builtin.env', 'NAUTOBOT_URL') }}"
    nautobot_token: "{{ lookup('ansible.builtin.env', 'NAUTOBOT_TOKEN') }}"
  tasks:
    - name: "TASK 10: CREATE REQUIRED ITEMS FOR DEVICES"
      networktocode.nautobot.manufacturer:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        name: "Cisco"
        state: present

    - name: "TASK 20: CREATE DEVICE TYPE"
      networktocode.nautobot.device_type:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        manufacturer: "Cisco"
        model: "Catalyst 9300"
        state: present

    - name: "TASK 30: CREATE LOCATION TYPE"
      networktocode.nautobot.location_type:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        name: "Site"
        content_types:
          - "dcim.device"

    - name: "TASK 40: CREATE LOCATION site01"
      networktocode.nautobot.location:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        name: "site01"
        location_type: "Site"
        status: "Active"

    - name: "TASK 40: CREATE LOCATION site02"
      networktocode.nautobot.location:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        name: "site02"
        location_type: "Site"
        status: "Active"

    - name: "TASK 50: CREATE ROLE"
      networktocode.nautobot.role:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        name: "Access Switch"
        content_types: 
          - "dcim.device"

    - name: "CREATE DEVICE 1"
      networktocode.nautobot.device:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        name: "dev01"
        device_type: "Catalyst 9300"
        location: "site01"
        status: Active
        role: "Access Switch"
        serial: "001"
        query_params:
          - serial

    - name: "CREATE DEVICE 2"
      networktocode.nautobot.device:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        name: "dev01"
        device_type: "Catalyst 9300"
        location: "site02"
        status: Active
        role: "Access Switch"
        serial: "002"
        query_params:
          - serial
```