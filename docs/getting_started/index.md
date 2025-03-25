# Contributing

The Nautobot Ansible modules are open source and also open for the community to contribute to the modules as well. 

At a minimum, Nautobot Ansible is intended to support the core data models for Nautobot. 

???+ note "Feature Requested"
    We welcome an auto-generated set of Ansible Modules from the API spec of Nautobot. This is currently an open call for help on this.

## MKDocs Contributions

MkDocs is used to provide the documentation, including the auto-documentation from Ansible. If there are any `markdown_extensions` that are to be used, please keep this alphabetized to help with identification.

## Generating Changelog Entries with Towncrier

This project utilizes [Towncrier](https://towncrier.readthedocs.io/en/stable/) to automate the generation of changelog entries. Towncrier ensures a consistent and organized changelog by requiring developers to create small, categorized news fragments for each change.

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

    * **Example:** If you are fixing a bug related to issue #123, you would create a file named `123.fixed`.

3.  **Write the Fragment Content:** The file should contain a concise description of the change. Keep the description brief and focused. If a change impacts users, write the description from the user's perspective.

    * **Example `123.fixed`:**
        ```
        Fixed an issue where the module failed to connect to the Nautobot API.
        ```

4.  **Commit the Fragment:** Add and commit the new fragment file to your Git branch.

### Generating the Changelog

When a new release is prepared, Towncrier will automatically generate the `CHANGELOG.md` file by aggregating all the news fragments. To generate the changelog locally, run the following command from the project root:

```bash
towncrier --draft
```
