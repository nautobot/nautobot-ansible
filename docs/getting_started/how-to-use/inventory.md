# Inventory

This page has a few examples that people have had questions about in the past. Please visit the [inventory plugin](../../networktocode.nautobot/inventory/index.md) documentation page for the full reference.

## Using Compose to Set `ansible_network_os` to Platform Network Driver

```yaml
---
plugin: networktocode.nautobot.inventory
compose:
  ansible_network_os: platform.network_driver
```

You can also use custom fields on the device or a nested object.

```yaml
---
plugin: networktocode.nautobot.inventory
compose:
  device_owner: custom_fields.device_owner
  ansible_network_os: platforms.custom_fields.ansible_network_os
```

## Using Keyed Groups to set `ansible_network_os` to Platform Network Driver

```yaml
---
plugin: networktocode.nautobot.inventory
keyed_groups:
  - key: platform
    prefix: "network_os"
    separator: "_"
```

!!! note
    The above examples are excerpts from the following [blog post](https://networktocode.com/blog/ansible-constructed-inventory/).


## Using Inventory Plugin Within AWX/Tower

This will cover the basic usage of the Nautobot inventory plugin within this collection.

1. Define `collections/requirements.yml` within a Git project.
2. AWX/Tower will download the collection on each run. This can be handled differently or excluded if storing Ansible Collections on the AWX/Tower box.
3. Define `inventory.yml` in Git project that adheres to inventory plugin structure.
4. Add Git project to AWX/Tower as a project.
5. Create inventory and select `source from project`.
6. Select the AWX/Tower project from Step 2
7. Select the `inventory.yml` file in the project from Step 3
8. Make sure your Tower installation uses Python 3 or select the proper `ANSIBLE ENVIRONMENT`
9. Click `Save` and sync source.
