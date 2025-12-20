# Inventory Integration Tests

This README is focused directly on the inventory integration tests

## Updating Inventory JSON Files

To update the inventory JSON files, you can run the `invoke integration` task with the `--update-inventories` flag.

```bash
invoke integration --update-inventories
```

> WARNING: This does not diff the files against any expected output, it simply overwrites the files with the latest data. You will need to manually verify the output is correct!

## Minimum Version Tested

Due to the static nature of the inventory tests as well as changes to models and API responses, the default minimum Nautobot version tested will generally be the last minor version that has been released.
This can be overridden by setting the `INVOKE_NAUTOBOT_ANSIBLE_MIN_INVENTORY_TEST_NAUTOBOT_VERSION` environment variable or `min_inventory_test_nautobot_version` setting in your `invoke.yml` file.
Similarly, the default minimum Ansible version tested will generally be the last minor version that has been released, and this can be overridden by setting the
`INVOKE_NAUTOBOT_ANSIBLE_MIN_INVENTORY_TEST_ANSIBLE_VERSION` environment variable or `min_inventory_test_ansible_version` setting in your `invoke.yml` file.
