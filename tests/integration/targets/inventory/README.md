# Inventory Integration Tests

This README is focused directly on the inventory integration tests

## Versioning

As Nautobot continues to move forward into new versions and add new models, the dynamic inventory that is returned can change.
In an attempt to combat this we need to incorporate a minimum and maximum version number for each test so that we can still test old versions while being able to adapt and iterate for new versions.
Currently we include the min and max versions as part of the filename to indicate which Nautobot versions the test is compatible with.

The pattern for all inventory test files should be as such: `test_{min version}-{max version}(optional extra moniker).yml`

The minimum version should be **inclusive** and the maximum version should be **exclusive**.
For example, the filename test_2-2.2.yml is for all versions greater than or equal to 2.0.0 and less than **but not equal** to 2.2.0.
Be sure to use "short" versions in the filename (`2.2` rather than `2.2.0`, `3` rather than `3.0.0`) dropping all trailing `.0`.

We use `sort` - using the `-V` flag to designate we are sorting version numbers - to do this and you can verify the validation yourself via `bash`:

```bash
# The pattern is min, current version, max
# If the sort doesn't change the order then it equates to True, but if the order changes than it equates to False.
> printf "%s\n%s\n%s\n" "2.0" "2.1.3" "2.2" | sort -V
2.0  # Minimum version got sorted to the top
2.1.3  # The current version got sorted to the middle, so this would equate to a match and run the test
2.2  # Maximum version got sorted to the bottom
> 
> printf "%s\n%s\n%s\n" "2.0" "2.2.3" "2.2" | sort -V
2.0  # Minimum version got sorted to the top
2.2  # Maximum version got sorted to the middle
2.2.3  # Notice that the current version got sorted to the end, so this would equate to not a match
> 
> printf "%s\n%s\n%s\n" "2.0" "2.2.0" "2.2" | sort -V
2.0  # Minimum version got sorted to the top
2.2  # Maximum version got sorted to the middle
2.2.0  # Just like in the last example, the full 2.2.0 got sorted above 2.2 so it would not match. The max version is exclusive.
> 
```

> Note: We expand the **current** version to the full major.minor.patch version automatically in CI so the sorting works correctly with this pattern. If you verify with printf, make sure you use the full version number for the current version, but the short versions for the min and max to match what automation will do.

## Updating Inventory JSON Files

To update the inventory JSON files, you can run the `invoke integration` task with the `--update-inventories` flag.

```bash
invoke integration --update-inventories
```

> WARNING: This does not diff the files against any expected output, it simply overwrites the files with the latest data. You will need to manually verify the output is correct!
