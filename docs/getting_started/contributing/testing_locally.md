# Testing Locally

## Testing Locally Overview

We provide the ability to run the tests locally to make sure the CI/CD pipeline will pass without having to wait for the CI/CD to run.

The tests are provided by enabling the environment using Poetry to provide the Invoke commands to run the tests.

## Pre-Push Checklist

Before pushing any change, run these fast checks. Most failures CI catches are reproducible locally in under a minute and don't require Docker.

```shell
# 1. pyproject.toml and poetry.lock are in sync
poetry check --lock

# 2. A towncrier changelog fragment exists for the issue/PR
poetry run towncrier check --compare-with origin/develop

# 3. Project lint -- this is what the CI `tests / lint` job runs
invoke lint
```

If any of those fail, fix and re-run before pushing.

!!! tip "Faster iteration while you work"

    `invoke lint` builds a Docker image, so the first run is not instant. While iterating you can run the individual linters it wraps directly:

    ```shell
    poetry run invoke check-versions
    poetry run ruff format --check .
    poetry run ruff check .
    poetry run pylint **/*.py
    ```

    Treat that as a fast pre-check, not a substitute. `invoke lint` is the authoritative mirror of CI — see the [CI Mirror Reference](#ci-mirror-reference) below.

For deeper coverage, also run the Docker-based `invoke unit` and, when modifying runtime behavior, `invoke integration`.

### When you bumped a dependency in `pyproject.toml`

```shell
# Poetry 2.x default behavior respects existing pins
poetry lock

# Confirm the diff is narrow (only the new/bumped dep and its transitives)
git diff --stat poetry.lock
git diff poetry.lock | head -100
```

Commit `poetry.lock` alongside `pyproject.toml`. CI checks them for sync and aborts otherwise.

## Invoke Tasks

You can get the list of available Invoke commands available for running the tests after launching `poetry shell`.

```shell
❯ poetry shell
```

```shell
❯ invoke --list
Available tasks:

  build             Build Nautobot docker image.
  cli               Launch a bash shell inside the running Nautobot container.
  createsuperuser   Create a new Nautobot superuser account (default: "admin"), will prompt for password.
  debug             Start Nautobot and its dependencies in debug mode.
  destroy           Destroy all containers and volumes.
  docs              Build and serve docs locally for development.
  galaxy-build      Build the collection.
  galaxy-install    Install the collection to ./collections.
  integration       Run all tests including integration tests
  lint              Run linting tools
  makemigrations    Perform makemigrations operation in Django.
  migrate           Perform migrate operation in Django.
  nbshell           Launch an interactive nbshell session.
  post-upgrade      Performs Nautobot common post-upgrade operations using a single entrypoint.
  restart           Gracefully restart all containers.
  start             Start Nautobot and its dependencies in detached mode.
  stop              Stop Nautobot and its dependencies.
  unit              Run unit tests
```

To start the Nautobot services to run the integration tests against, run the `invoke start` command.

```shell
❯ invoke start
Starting Nautobot in detached mode...
Running docker-compose command "up --detach"
Creating network "nautobot_ansible_default" with the default driver
Creating nautobot_ansible_postgres_1 ... done
Creating nautobot_ansible_redis_1    ... done
Creating nautobot_ansible_nautobot_1 ... done
Creating nautobot_ansible_worker_1   ... done
```

You can then run `invoke integration` to run the integration tests against Nautobot.

```
❯ invoke integration
```

You can use `-t` to run only specific tagged tests, or `-s` to skip specific test categories. Use `-h` to see all available options.

```shell
# Run only graphql_info integration tests
❯ invoke integration -t graphql_info

# Run only graphql_info and graphql_facts tests
❯ invoke integration -t graphql_info -t graphql_facts

# Skip lint and sanity, only run integration tests
❯ invoke integration -s lint -s sanity

# See all available options
❯ invoke integration -h
```

## Using Environment Variables

You can use the following environment variables to test against different Python or Nautobot versions.

- **INVOKE_NAUTOBOT_ANSIBLE_NAUTOBOT_VER**
- **INVOKE_NAUTOBOT_ANSIBLE_PYTHON_VER**

## Using Docker Compose Overrides

If you require changing any of the defaults found in `docker-compose.yml`, create a file inside the `development` directory called `docker-compose.override.yml` and add this file to the `compose_files` setting in your `invoke.yml` file, for example:

```yaml
nautobot_ansible:
  compose_files:
    - "docker-compose.yml"
    - "docker-compose.override.yml"
```

This file will override any configuration in the main `docker-compose.yml` file, without making changes to the repository.

Please see the [official documentation on extending Docker Compose](https://docs.docker.com/compose/extends/) for more information.

## CI Mirror Reference

Each invoke task corresponds to one or more CI jobs:

| Invoke task | CI job | What it runs |
|---|---|---|
| `invoke lint` | `tests / lint` | `invoke check-versions` + `ruff format .` + `ruff check .` + `pylint **/*.py` inside the lint container |
| `invoke unit` | `tests / unit (3.12/3.13/3.14)` | Project lint + `ansible-test sanity --requirements` + `ansible-lint` + unit tests |
| `invoke integration` | `tests / integration_partial` and `tests / integration_full` | Full integration suite against a real Nautobot instance |
| `invoke galaxy-build` | (release workflow `build_collection` step) | Generates `requirements.txt`, builds the collection tarball, cleans up |

## Gotchas

These are easy to miss and lead to the "CI fails after a clean local run" pattern:

1. **Two pylint surfaces, different scopes.** CI runs pylint twice:
    - `tests / lint` runs `pylint **/*.py` from the project root. In bash without `shopt -s globstar`, `**` is plain `*`, so the glob matches files exactly one directory deep (`development/foo.py`, `plugins/foo.py`, `tests/foo.py`). Files in `tests/unit/foo.py` are NOT covered here.
    - `tests / unit` runs `ansible-test sanity --test pylint`, which uses its own pylint configuration and scans every `.py` file in the collection layout including `tests/unit/`.

    A clean `invoke lint` does NOT imply a clean `invoke unit`. Run both before pushing.

2. **Ansible-core version skew.** `pyproject.toml` pins `ansible-core>=2.18,<2.20`. Your local Poetry environment may resolve to 2.19 while CI runs 2.18. Newer ansible-core has stricter pylint rules (for example, 2.19's `disallowed-name` rule). If a pylint issue you see locally points at code that has been on `develop` for months, check `git blame` before chasing it -- it is probably 2.19-only and won't fail CI.

3. **Convention warnings still fail the build.** `pylint`'s "Your code has been rated at X/10" line is informational. Any `C0xxx` (convention) message exits non-zero and fails the Docker build for the lint job. Don't trust the rating; resolve every reported line.

4. **`requirements.txt` is generated, not tracked.** The root `requirements.txt` consumed by Red Hat Automation Hub is produced from `pyproject.toml` by `development/generate_requirements.py` at build time. See the [Python Dependencies](python_dependencies.md) page for details.

5. **The lint Docker stage builds a fresh image every run.** First `invoke lint` is slow (around 5 minutes). Subsequent runs are faster due to Docker layer caching, but expect the first one to take a while.

## Using a Custom Nautobot Init File

If you require using a custom Nautobot init file, you can create a file inside the `development` directory called `nautobot.sql` and add this file to the `volumes` setting in your `docker-compose.override.yml` file, for example:

```yaml
---
services:
  postgres:
    volumes:
      - "./nautobot.sql:/docker-entrypoint-initdb.d/nautobot.sql"
```
