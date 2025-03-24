# Creating Changelog Fragments

All pull requests to `next` or `develop` must include a changelog fragment file in the `./changes` directory. To create a fragment, use your GitHub issue (or PR) number and fragment type as the filename. For example, `2362.added`. Valid fragment types are `added`, `changed`, `dependencies`, `deprecated`, `documentation`, `fixed`, `housekeeping`, `removed`, and `security`. Changes that are not directly related to a specific issue can be added with a filename that starts with a plus sign in the format of `+feature.type` (e.g., `+docs-update.housekeeping`).

Inside the file should be your change summary. Change summaries should be complete sentences, starting with a capital letter and ending with a period, and be in past tense. The change summary will be added to `CHANGELOG.md` in plain text preceded by a link to the GitHub issue (if applicable) under the heading of the fragment type. Each line of the change fragment will generate a single change entry in the release notes. Use multiple lines in the same file if your change needs to generate multiple release notes in the same category. If the change needs to create multiple entries in separate categories, create multiple files.

!!! example

    **Wrong**

    ```plaintext title="changes/1234.fixed"
    fix critical bug in documentation
    ```

    **Right**

    ```plaintext title="changes/1234.fixed"
    Fixed critical bug in documentation.
    ```

!!! example "Multiple Entry Example"

    This will generate 2 entries in the `fixed` category and one entry in the `changed` category.

    ```plaintext title="changes/1234.fixed"
    Fixed critical bug in documentation.
    Fixed release notes generation.
    ```

    ```plaintext title="changes/1234.changed"
    Changed release notes generation.
    ```
