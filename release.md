# Release Updates

## Release Checklist

- poetry version major/minor/patch
- poetry update
- Updated changelogs/changelog.yaml
- Updated CHANGELOG.md
- Updated version in galaxy.yml


## Update Docs

!!! warn
    These are older release step, should follow the release checklist above in most cases.

1. Update the permissions on docs/plugins to 0755

```
sudo chmod -R 0755 docs/plugins
```

2. Execute make-docs.sh from hacks

```
hacking/make-docs.sh
```

## CHANGELOG

3. Update the file `changelogs/changelog.yaml` to include details about the changes made.
4. Run command `antsibull-changelog release --version 3.0.0` to create the files within documentation
