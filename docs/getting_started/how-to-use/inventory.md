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

## Using Computed Fields

[Computed fields](https://docs.nautobot.com/projects/core/en/stable/user-guide/platform-functionality/computedfield/) are Jinja2 templates that Nautobot renders when an object is read. The REST API only returns them when they are explicitly requested, so the inventory plugin does not fetch them unless you ask it to.

```yaml
---
plugin: networktocode.nautobot.inventory
computed_fields: true
```

Each host then gets a `computed_fields` host var holding every computed field that applies to it, keyed by the computed field's key. Set `flatten_computed_fields: true` to promote each key to a host var of its own instead, and use `compose` to lift a single field to a name of your choosing.

```yaml
---
plugin: networktocode.nautobot.inventory
computed_fields: true
compose:
  device_summary: computed_fields.my_device_summary
```

You can also build groups from computed fields. Each key/value pair becomes its own group, named `computed_field_<key>_<value>`, or `<key>_<value>` when `group_names_raw` is enabled.

```yaml
---
plugin: networktocode.nautobot.inventory
computed_fields: true
group_by:
  - computed_fields
```

Grouping requires `computed_fields: true`; it does not turn the option on for you.

!!! warning
    Two things to keep in mind. Nautobot renders every computed field for every object on every request, so enabling this against a large inventory adds real server-side work — leave it off unless you need it. And because computed field values are arbitrary rendered text, `group_by` on a field that renders free-form prose produces unusable group names; `keyed_groups` on a single composed field is the precise alternative.

!!! note
    Ansible keys the inventory cache on the inventory file's path, not on the options inside it. If you are running with `cache: true` and you turn `computed_fields` on, you will keep getting cached hosts without computed fields until the cache entry expires or you flush it.

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
