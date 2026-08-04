# Python Dependencies

This page explains how runtime Python dependencies are declared, where the canonical version constraints live, and how the `requirements.txt` files consumed by Execution Environment builds are produced.

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

## Why we generate `requirements.txt` files

`ansible-builder` resolves a collection's Python runtime dependencies from a `requirements.txt` shipped inside the published collection tarball, so it can install them when constructing an Execution Environment (EE). This collection ships the file in **two** locations:

| Path | Consumed by |
|---|---|
| `meta/requirements.txt` | The standard location `ansible-builder` discovers for any collection pulled into an EE. |
| `requirements.txt` (collection root) | Additionally required by Red Hat Automation Hub's certification tooling. |

Both files are generated from `pyproject.toml` and have identical content. **Neither is committed to the repo** (both are gitignored); they are regenerated on every build and removed afterward.

This avoids two failure modes:

1. **Drift.** A hand-maintained `requirements.txt` inevitably drifts from `pyproject.toml`. The generator forces them to stay in sync at build time.
2. **Wrong shape.** Red Hat Partner Engineering requires floor-only specifiers (`>=X.Y.Z`): no exact pins (`==`), no upper caps (`<=`). Poetry constraints use caret/tilde/comma-separated specs that would not satisfy that rule directly. The generator translates them.

## How the generator works

The generator lives at `development/generate_requirements.py`. It reads `[tool.poetry.dependencies]` from `pyproject.toml` via `tomllib` and emits a floor-only line for **every** declared dependency, except the small set that must not ship in an EE. This keeps `pyproject.toml` the single source of truth: a newly added runtime dependency flows into the generated files automatically, with no change to the script.

The only dependencies excluded from the output (`EXCLUDED_DEPS` in the script) are:

| Excluded package | Why it is not emitted |
|---|---|
| `python` | An interpreter constraint, not an installable package. |
| `ansible-core` | Provided by the EE base image; a collection must not pin its own `ansible-core`, or it conflicts with other collections sharing the EE. |
| `asyncio` | Part of the standard library since Python 3.4. The PyPI `asyncio` package is a Python 3.3 backport that shadows the stdlib module and breaks modern runtimes if installed. |

Everything else in `[tool.poetry.dependencies]` is emitted. Today that resolves to the packages the collection imports directly:

| Package | Used by |
|---|---|
| `pynautobot` | `plugins/action/*`, `plugins/lookup/*` |
| `requests` | `plugins/action/{query_graphql,graphql_info,graphql_facts}.py` |
| `netutils` | `plugins/inventory/gql_inventory.py` |
| `aiohttp` | `extensions/eda/plugins/event_source/nautobot_changelog.py` |

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

The generator is wired into the build flow so contributors and CI do not have to remember to run it.

### Local builds

`invoke galaxy-build` automatically generates both requirements files, builds the collection tarball, and removes the files afterward. You do not need to invoke the generator separately:

```bash
poetry run invoke galaxy-build
```

If you want to inspect the generated content without building:

```bash
poetry run invoke generate-requirements
cat requirements.txt
cat meta/requirements.txt
rm requirements.txt meta/requirements.txt
```

### Release CI

The release workflow (`.github/workflows/trigger_release.yml`) calls the generator before `ansible-galaxy collection build`, so the published tarball uploaded to GitHub Releases, Ansible Galaxy, and Red Hat Automation Hub always contains up-to-date requirements files.

## Updating dependencies

To bump a dependency version:

1. Run `poetry add <package>@^X.Y.Z` (or edit `pyproject.toml` directly) to update the declared range.
2. Run `poetry lock` to regenerate `poetry.lock`.
3. Commit `pyproject.toml` and `poetry.lock`.

The generated requirements files will automatically reflect the new floor on the next build.

To add a new direct runtime import (i.e., the collection starts importing a new external package):

1. Add the package to `[tool.poetry.dependencies]` in `pyproject.toml`.
2. That is it. The generator emits it automatically. Only edit `EXCLUDED_DEPS` in `development/generate_requirements.py` if the new dependency must **not** ship in an EE (as with `python`, `ansible-core`, and `asyncio`), and add a matching case to `tests/unit/test_generate_requirements.py`.

## Reference

- Partner-engineering email (2026-05-26) that introduced the `requirements.txt` requirement: tracked in issue #751.
- `ansible-builder` documentation on dependency resolution: <https://ansible.readthedocs.io/projects/builder/en/latest/definition/#dependencies>.
