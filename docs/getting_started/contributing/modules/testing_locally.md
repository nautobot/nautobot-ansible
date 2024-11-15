==========================
Testing Locally
==========================

Testing Locally Overview
------------------------------

We provide the ability to run the tests locally to make sure the CI/CD pipeline will pass without having to wait for the CI/CD to run.

The tests are provided by enabling the environment using Poetry to provide the Invoke commands to run the tests.

Invoke Tasks
----------------------

You can get the list of available Invoke commands available for running the tests after launching `poetry shell`.

```shell
❯ poetry shell
```

```shell
❯ invoke --list
Available tasks:

  cli               Launch a bash shell inside the running Nautobot container.
  createsuperuser   Create a new Nautobot superuser account (default: "admin"), will prompt for password.
  debug             Start Nautobot and its dependencies in debug mode.
  destroy           Destroy all containers and volumes.
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

Using Environment Variables
------------------------------

You can use the following environment variables to test against different Python or Nautobot version.

- **INVOKE_NAUTOBOT_ANSIBLE_NAUTOBOT_VER**
- **INVOKE_NAUTOBOT_ANSIBLE_PYTHON_VER**
