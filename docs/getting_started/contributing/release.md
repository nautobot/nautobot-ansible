# Release Updates

## Release Checklist

Here are the general steps to follow to release a new version of the collection.

Create a new branch for the release based on the `develop` branch. An example branch name would be `release_v5.10.0`.
Follow these steps to update the version and generate the release notes:

- Run `poetry version [major/minor/patch]` to update the version
- Run `poetry update` to update the dependencies
- Run `invoke generate-release-notes` to automatically update `CHANGELOG.md` with the new version and release notes
- (Optional) Add a Release Summary to the new section in `CHANGELOG.md` as desired
- Manually update `changelogs/changelog.yaml` following the format of the previous entries (per Ansible Collection guidelines)
- Manually update the version in `galaxy.yml` to match the new version from poetry

Next, create a PR on GitHub from your release branch to the `develop` branch.
Once the PR is approved and merged, create a PR on GitHub from the `develop` branch to the `main` branch for the release.
Lastly, once that PR is approved and merged, create a new release on GitHub with the following parameters:

- **Choose a tag**: Type in the new version from poetry preceded by a `v` (e.g., `v5.10.0`) and select the option "Create a new tag: v#.#.# on publish"
- **Target**: Select the `main` branch
- **Previous tag**: You can leave this as `auto`
- Click **Generate release notes** to automatically generate the title and release notes for the new version.
- Ensure the **Set as the latest release** checkbox is checked

!!! note
    You may remove any generated bullet points in "What's Changed" that contain the PRs for the above release steps.

## LTM Release Checklist

Here are the general steps to follow to release a new LTM version of the collection.

Create a new branch for the release based on the `ltm-1.6` branch.
Follow these steps to update the version and generate the release notes:

- Run `poetry version patch` to update the version
- Run `poetry update` to update the dependencies
- Manually update `CHANGELOG.md` to include the new version and release notes
- Manually update `changelogs/changelog.yaml` following the format of the previous entries (per Ansible Collection guidelines)
- Manually update the version in `galaxy.yml` to match the new version from poetry

Next, create a PR on GitHub from your release branch to the `ltm-1.6` branch.
Once the PR is approved and merged, create a new release on GitHub with the following parameters:

- **Choose a tag**: Type in the new version from poetry preceded by a `v` (e.g., `v4.5.3`) and select the option "Create a new tag: v#.#.# on publish"
- **Target**: Select the `ltm-1.6` branch
- **Previous tag**: Find and select the previous tag from the `ltm-1.6` branch (e.g., `v4.5.2`)
- Click **Generate release notes** to automatically generate the title and release notes for the new version.
- **UNCHECK** the **Set as the latest release** checkbox as this is not the latest release for the collection

!!! danger
    Do not check the **Set as the latest release** checkbox for LTM releases as this is not the latest release for the collection.
