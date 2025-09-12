# Testing Locally

## Testing Locally Overview

We provide the ability to run the tests locally to make sure the CI/CD pipeline will pass without having to wait for the CI/CD to run.

The tests are provided by enabling the environment using Poetry to provide the Invoke commands to run the tests.

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

## Using Environment Variables

You can use the following environment variables to test against different Python or Nautobot version.

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

## Using a Custom Nautobot Init File

If you require using a custom Nautobot init file, you can create a file inside the `development` directory called `nautobot.sql` and add this file to the `volumes` setting in your `docker-compose.override.yml` file, for example:

```yaml
---
services:
  postgres:
    volumes:
      - "./nautobot.sql:/docker-entrypoint-initdb.d/nautobot.sql"
```
