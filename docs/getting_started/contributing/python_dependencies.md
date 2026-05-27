# Python Dependencies

This page explains how runtime Python dependencies are declared, where the canonical version constraints live, and how a root-level `requirements.txt` is produced for Red Hat Automation Hub Execution Environment builds.

## Single source of truth: `pyproject.toml`

All runtime and development dependencies for this collection are declared in `pyproject.toml` under `[tool.poetry.dependencies]`. Poetry resolves and locks them in `poetry.lock`. Contributors should add or update Python dependencies there, not in a hand-maintained `requirements.txt`.

Example:

```toml
[tool.poetry.dependencies]
python = ">=3.11,<4.0"
netutils = "^1.2"
pynautobot = ">=3.0.0,<4.0.0"
ansible-core = ">=2.18,<2.20"
aiohttp = "^3.11.13"
requests = "^2.28.0"
```

## Why we also publish a `requirements.txt`

Red Hat Automation Hub's `ansible-builder` reads a root-level `requirements.txt` from the published collection tarball to install Python deps when constructing an Execution Environment (EE). Without it, EE builds that include this collection fail to resolve `pynautobot`, `requests`, `netutils`, and `aiohttp`, leaving end users to identify and install them manually.

So we ship a `requirements.txt` inside the tarball, but we **do not commit it to the repo**. It's regenerated from `pyproject.toml` on every build, then removed.

This avoids two failure modes:

1. **Drift.** A hand-maintained `requirements.txt` inevitably drifts from `pyproject.toml`. The generator forces them to stay in sync at build time.
2. **Wrong shape.** Red Hat Partner Engineering specifically requires floor-only specifiers (`>=X.Y.Z`); no exact pins (`==`), no upper caps (`<=`). Poetry constraints use caret/tilde/comma-separated specs that wouldn't satisfy that rule directly. The generator translates them.

## How the generator works

The generator lives at `development/generate_requirements.py`. It reads `[tool.poetry.dependencies]` from `pyproject.toml` via `tomllib`, picks the subset of dependencies that the collection actually imports at runtime, and emits a floor-only `requirements.txt` at the repo root.

The current EE-relevant dependency list (kept inline at the top of the script):

| Package | Used by |
|---|---|
| `pynautobot` | `plugins/action/*`, `plugins/lookup/*` |
| `requests` | `plugins/action/{query_graphql,graphql_info,graphql_facts}.py` |
| `netutils` | `plugins/inventory/gql_inventory.py` |
| `aiohttp` | `extensions/eda/plugins/event_source/nautobot_changelog.py` |

If a new plugin or extension adds a direct import of an external package, update the `EE_DEPS` list in the generator script.

### Version translation rules

The generator's `floor()` function converts each Poetry constraint to a `>=X.Y.Z` line:

| Poetry constraint | Emitted line |
|---|---|
| `^1.2.3` (caret) | `pkg>=1.2.3` |
| `~1.2.3` (tilde) | `pkg>=1.2.3` |
| `>=3.0.0,<4.0.0` | `pkg>=3.0.0` |
| `>=2.28.0` | `pkg>=2.28.0` |
| `1.2.3` (exact) | `pkg>=1.2.3` |

Upper caps are intentionally stripped. Red Hat Partner Engineering guidance states that caps cause conflicts when multiple collections share an Execution Environment.

## When the generator runs

The generator is wired into the build flow so contributors and CI don't have to remember to run it.

### Local builds

`invoke galaxy-build` automatically generates `requirements.txt`, builds the collection tarball, and removes the file afterward. You don't need to invoke the generator separately:

```bash
poetry run invoke galaxy-build
```

If you want to inspect the generated content without building:

```bash
poetry run invoke generate-requirements
cat requirements.txt
rm requirements.txt
```

### Release CI

The release workflow (`.github/workflows/trigger_release.yml`) calls the generator before `ansible-galaxy collection build`, so the published tarball uploaded to GitHub Releases, Ansible Galaxy, and Red Hat Automation Hub always contains an up-to-date `requirements.txt`.

## Updating dependencies

To bump a dependency version:

1. Run `poetry add <package>@^X.Y.Z` (or edit `pyproject.toml` directly) to update the declared range.
2. Run `poetry update <package>` to regenerate `poetry.lock`.
3. Commit `pyproject.toml` and `poetry.lock`.

The generated `requirements.txt` will automatically reflect the new floor on the next build.

To add a new direct runtime import (i.e., the collection starts importing a new external package):

1. Add the package to `[tool.poetry.dependencies]` in `pyproject.toml`.
2. Add the package name to the `EE_DEPS` list in `development/generate_requirements.py`, with a comment noting where it's imported.
3. Add a test case under `tests/unit/test_generate_requirements.py::TestEEDepsAllowlist` if the expected set needs updating.

## Reference

- Partner-engineering email (2026-05-26) that introduced the `requirements.txt` requirement: tracked in issue #751.
- `ansible-builder` documentation on dependency resolution: <https://ansible.readthedocs.io/projects/builder/en/latest/definition/#dependencies>.
