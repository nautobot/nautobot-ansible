# Inline Many-to-Many Associations

+++ 6.2.0

Many Nautobot models have many-to-many (M2M) relationships with other models. For example, a device can be associated with multiple VRFs, a location can have multiple prefixes, and a secrets group can contain multiple secrets.

Previously, managing these associations required using separate standalone modules (e.g., `vrf_device_assignment`, `prefix_location`, `secrets_groups_association`). Now you can manage them inline on the parent module using the M2M field options.

## Supported Parent Modules and Fields

| Parent Module | M2M Field | Child Object Key | Description |
|---|---|---|---|
| `device` | `vrfs` | `vrf` | VRF assignments |
| `device` | `clusters` | `cluster` | Cluster assignments |
| `virtual_machine` | `vrfs` | `vrf` | VRF assignments |
| `virtual_device_context` | `vrfs` | `vrf` | VRF assignments |
| `device_interface` | `ip_addresses` | `ip_address` | IP address to interface |
| `vm_interface` | `ip_addresses` | `ip_address` | IP address to VM interface |
| `location` | `prefixes` | `prefix` | Prefix to location |
| `location` | `vlans` | `vlan` | VLAN to location |
| `cloud_network` | `prefixes` | `prefix` | Cloud network prefix assignments |
| `cloud_service` | `cloud_networks` | `cloud_network` | Cloud service network assignments |
| `secrets_group` | `secrets` | `secret` | Secrets group associations |
| `dynamic_group` | `static_group_associations` | `associated_object_type` / `associated_object_id` | Static group memberships |
| `custom_field` | `custom_field_choices` | `value` | Custom field choices |
| `metadata_type` | `metadata_choices` | `value` | Metadata type choices |
| `provider` | `provider_networks` | `name` | Provider networks |

## M2M Field Structure

All M2M fields follow the same structure:

```yaml
<m2m_field>:
  state: merge  # merge (default), replace, or delete
  objects:
    - <child_key>: "value"
    - <child_key>: "another value"
```

### States

- **merge** (default): Adds the specified associations without removing existing ones. Safe for incremental changes.
- **replace**: Enforces exactly the listed associations. Any existing associations not in the list are removed.
- **delete**: Removes only the specified associations. Other existing associations are left intact.

## Basic Examples

### Adding VRFs to a Device

```yaml
- name: Create a device with VRF associations
  networktocode.nautobot.device:
    url: "{{ nautobot_url }}"
    token: "{{ nautobot_token }}"
    name: "my-router"
    device_type: "Cisco CSR1000v"
    role: "Router"
    location: "Main Site"
    status: "Active"
    vrfs:
      objects:
        - vrf: "Management VRF"
        - vrf: "Production VRF"
    state: present
```

Since no `state` is specified on the `vrfs` field, it defaults to `merge` -- the VRFs are added without affecting any other existing VRF associations.

### Adding IP Addresses to an Interface

The child key accepts either a simple string or a dictionary for more specific lookups:

```yaml
# Simple string -- looks up the IP address by address
- name: Associate IP addresses with an interface
  networktocode.nautobot.device_interface:
    url: "{{ nautobot_url }}"
    token: "{{ nautobot_token }}"
    device: "my-router"
    name: "GigabitEthernet0/0"
    ip_addresses:
      objects:
        - ip_address: "10.0.0.1/24"
    state: present

# Dictionary -- useful when disambiguation is needed (e.g., multiple namespaces)
- name: Associate IP address with namespace specified
  networktocode.nautobot.device_interface:
    url: "{{ nautobot_url }}"
    token: "{{ nautobot_token }}"
    device: "my-router"
    name: "GigabitEthernet0/0"
    ip_addresses:
      objects:
        - ip_address:
            address: "10.0.0.1/24"
            namespace: "Production"
    state: present
```

### Adding Secrets to a Secrets Group

Some M2M associations have extra fields beyond just the child identifier. For secrets group associations, `access_type` and `secret_type` are part of the association itself:

```yaml
- name: Create secrets group with secret associations
  networktocode.nautobot.secrets_group:
    url: "{{ nautobot_url }}"
    token: "{{ nautobot_token }}"
    name: "Device Credentials"
    secrets:
      objects:
        - secret: "admin-username"
          access_type: "SSH"
          secret_type: "username"
        - secret: "admin-password"
          access_type: "SSH"
          secret_type: "password"
    state: present
```

## Managing Association State

### Merge (Default)

Merge adds new associations without removing existing ones. Running the same task twice is idempotent.

```yaml
# First run: adds VRF-A
- name: Add first VRF
  networktocode.nautobot.device:
    url: "{{ nautobot_url }}"
    token: "{{ nautobot_token }}"
    name: "my-router"
    vrfs:
      objects:
        - vrf: "VRF-A"
    state: present

# Second run: adds VRF-B, VRF-A is untouched
- name: Add second VRF
  networktocode.nautobot.device:
    url: "{{ nautobot_url }}"
    token: "{{ nautobot_token }}"
    name: "my-router"
    vrfs:
      objects:
        - vrf: "VRF-B"
    state: present
# Result: device has both VRF-A and VRF-B
```

### Replace

Replace enforces exactly the listed set of associations. Any existing associations not in the list are removed.

```yaml
# Device currently has VRF-A and VRF-B
- name: Replace all VRFs with only VRF-C
  networktocode.nautobot.device:
    url: "{{ nautobot_url }}"
    token: "{{ nautobot_token }}"
    name: "my-router"
    vrfs:
      state: replace
      objects:
        - vrf: "VRF-C"
    state: present
# Result: device has only VRF-C (VRF-A and VRF-B removed)
```

### Delete

Delete removes only the specified associations. Other associations are left intact.

```yaml
# Device currently has VRF-A and VRF-B
- name: Remove only VRF-B
  networktocode.nautobot.device:
    url: "{{ nautobot_url }}"
    token: "{{ nautobot_token }}"
    name: "my-router"
    vrfs:
      state: delete
      objects:
        - vrf: "VRF-B"
    state: present
# Result: device has only VRF-A
```

## Diff Output

When M2M fields change, the diff output includes the before and after state as sorted lists of child object UUIDs:

```json
{
    "diff": {
        "before": {
            "vrfs": ["<uuid-of-vrf-a>"]
        },
        "after": {
            "vrfs": ["<uuid-of-vrf-a>", "<uuid-of-vrf-b>"]
        }
    }
}
```
