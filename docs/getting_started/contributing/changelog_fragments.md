# Creating Changelog Fragments

## Generating Changelog Entries with Towncrier

This project utilizes [Towncrier](https://towncrier.readthedocs.io/en/stable/) to automate the generation of changelog entries. Towncrier ensures a consistent and organized changelog by requiring developers to create small, categorized news fragments for each change.

### Creating Changelog Fragments

All pull requests to `next` or `develop` must include a changelog fragment file in the `./changes` directory. To create a fragment, use your GitHub issue (or PR) number and fragment type as the filename. For example, `2362.added`.

### How to Create a News Fragment

1.  **Navigate to the `changes` Directory:** All news fragments are stored in the `changes` directory at the root of the repository.

2.  **Create a New File:** Create a new file within the appropriate subdirectory based on the type of change. The filename should follow the pattern `<issue_number>.<extension>`, where `<issue_number>` is the GitHub issue or pull request number associated with the change, and `<extension>` corresponds to the fragment type.

    * **Available Fragment Types:**
        * `added`: New features or functionality.
        * `changed`: Modifications to existing features.
        * `dependencies`: Updates to project dependencies.
        * `deprecated`: Features marked for future removal.
        * `documentation`: Changes to project documentation.
        * `fixed`: Bug fixes.
        * `housekeeping`: Internal changes (e.g., refactoring, testing).
        * `removed`: Removal of features or functionality.
        * `security`: Security-related fixes.
    * Changes that are not directly related to a specific issue can be added with a filename that starts with a plus sign in the format of `+feature.type` (e.g., `+docs-update.housekeeping`).

3.  **Write the Fragment Content:** Inside the file should be your change summary. Change summaries should be complete sentences, starting with a capital letter and ending with a period, and be in past tense. The change summary will be added to `CHANGELOG.md` in plain text preceded by a link to the GitHub issue (if applicable) under the heading of the fragment type. Each line of the change fragment will generate a single change entry in the release notes. Use multiple lines in the same file if your change needs to generate multiple release notes in the same category. If the change needs to create multiple entries in separate categories, create multiple files.

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


4.  **Commit the Fragment:** Add and commit the new fragment file to your Git branch.

### Generating the Changelog

When a new release is prepared, Towncrier will automatically generate the `CHANGELOG.md` file by aggregating all the news fragments. To generate the changelog locally, run the following command from the project root:

```bash
towncrier --draft
