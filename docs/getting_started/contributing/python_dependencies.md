# Python Dependencies

This page explains how runtime Python dependencies are declared, where the canonical version constraints live, and how the `requirements.txt` files consumed by Execution Environment builds are produced and kept in sync.

## Single source of truth: `pyproject.toml`

All runtime and development dependencies for this collection are declared in `pyproject.toml` under `[tool.poetry.dependencies]`. Poetry resolves and locks them in `poetry.lock`. Contributors should add or update Python dependencies there, never by hand-editing a `requirements.txt`.

Example:

```toml
[tool.poetry.dependencies]
python = ">=3.12,<4.0"
netutils = "^1.2"
pynautobot = ">=3.0.0,<4.0.0"
ansible-core = ">=2.18,<2.21"
aiohttp = "^3.11.13"
requests = "^2.28.0"
```

## Why the `requirements.txt` files are generated

`ansible-builder` resolves a collection's Python runtime dependencies from a `requirements.txt` shipped with the collection, so it can install them when constructing an Execution Environment (EE). This collection ships the file in **two** locations:

| Path | Consumed by |
|---|---|
| `meta/requirements.txt` | The file `meta/execution-environment.yml` points at. `ansible-builder` reads it for any collection pulled into an EE. |
| `requirements.txt` (collection root) | Additionally required by Red Hat Automation Hub's certification tooling. |

Both files are generated from `pyproject.toml` and have identical content. **Both are committed.** `ansible-builder` follows the pointer in `meta/execution-environment.yml` and fails hard if the target is missing, so the files must exist in a plain git checkout (for example an EE definition that pulls this collection from a git URL), not only in the published tarball.

Committing derived files is safe because CI enforces that they match `pyproject.toml`. This avoids two failure modes:

1. **Drift.** A hand-maintained `requirements.txt` inevitably drifts from `pyproject.toml`. The `tests / lint` job runs the generator in check mode and fails when the committed files differ from what `pyproject.toml` produces.
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

## Keeping the files in sync

Two invoke tasks wrap the generator:

```bash
# Rewrite both files from pyproject.toml
poetry run invoke generate-requirements

# Verify the committed files match pyproject.toml; exit 1 and name the stale files otherwise
poetry run invoke generate-requirements --check
```

The check runs in three places, so drift cannot reach a release:

- **`invoke lint`** runs `invoke generate-requirements --check` inside the lint container, right after `invoke check-versions`. This is what the CI `tests / lint` job executes, so a pull request that changes `pyproject.toml` without regenerating the files fails with `Out of date with pyproject.toml: requirements.txt, meta/requirements.txt`.
- **`invoke galaxy-build`** runs the check before `ansible-galaxy collection build`, so a local tarball cannot be built from stale files.
- **The `galaxy_importer` CI job** builds the tarball from the checkout and runs `galaxy-importer` against it, the same checks `console.redhat.com` runs at publish time. Because the files are committed, neither this job nor the release workflow needs a build-time generation step.

## Updating dependencies

To bump a dependency version:

1. Run `poetry add <package>@^X.Y.Z` (or edit `pyproject.toml` directly) to update the declared range.
2. Run `poetry lock` to regenerate `poetry.lock`.
3. Run `poetry run invoke generate-requirements` to regenerate both requirements files.
4. Commit `pyproject.toml`, `poetry.lock`, `requirements.txt`, and `meta/requirements.txt` together.

To add a new direct runtime import (i.e., the collection starts importing a new external package):

1. Add the package to `[tool.poetry.dependencies]` in `pyproject.toml` and run `poetry lock`.
2. Run `poetry run invoke generate-requirements` and commit the result. The generator emits the new package automatically. Only edit `EXCLUDED_DEPS` in `development/generate_requirements.py` if the new dependency must **not** ship in an EE (as with `python`, `ansible-core`, and `asyncio`), and add a matching case to `tests/unit/test_generate_requirements.py`.

## Reference

- Partner-engineering email (2026-05-26) that introduced the `requirements.txt` requirement: tracked in issue #751.
- `ansible-builder` documentation on dependency resolution: <https://ansible.readthedocs.io/projects/builder/en/latest/definition/#dependencies>.
