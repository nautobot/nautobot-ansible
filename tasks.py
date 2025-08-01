"""Tasks for use with Invoke."""

import os

from invoke import Collection, Exit
from invoke import task as invoke_task


def is_truthy(arg):
    """Convert "truthy" strings into Booleans.

    Examples:
        >>> is_truthy('yes')
        True
    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1; false values are n, no,
        f, false, off and 0. Raises ValueError if val is anything else.
    """
    if isinstance(arg, bool):
        return arg

    val = str(arg).lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(f"Invalid truthy value: `{arg}`")


# Use pyinvoke configuration for default values, see http://docs.pyinvoke.org/en/stable/concepts/configuration.html
# Variables may be overwritten in invoke.yml or by the environment variables INVOKE_NAUTOBOT_ANSIBLE_xxx
namespace = Collection("nautobot_ansible")
namespace.configure(
    {
        "nautobot_ansible": {
            "nautobot_ver": "2.0.0",
            "project_name": "nautobot_ansible",
            "python_ver": "3.11",
            "local": False,
            "compose_dir": os.path.join(os.path.dirname(__file__), "development"),
            "compose_files": ["docker-compose.yml"],
        }
    }
)


def task(function=None, *args, **kwargs):
    """Task decorator to override the default Invoke task decorator and add each task to the invoke namespace."""

    def task_wrapper(function=None):
        """Wrapper around invoke.task to add the task to the namespace as well."""
        if args or kwargs:
            task_func = invoke_task(*args, **kwargs)(function)
        else:
            task_func = invoke_task(function)
        namespace.add_task(task_func)
        return task_func

    if function:
        # The decorator was called with no arguments
        return task_wrapper(function)
    # The decorator was called with arguments
    return task_wrapper


def docker_compose(context, command, **kwargs):
    """Helper function for running a specific docker compose command with all appropriate parameters and environment.

    Args:
        context (obj): Used to run specific commands
        command (str): Command string to append to the "docker compose ..." command, such as "build", "up", etc.
        **kwargs: Passed through to the context.run() call.
    """
    build_env = {
        "NAUTOBOT_VER": context.nautobot_ansible.nautobot_ver,
        "PYTHON_VER": context.nautobot_ansible.python_ver,
    }
    compose_command = f'docker compose --project-name {context.nautobot_ansible.project_name} --project-directory "{context.nautobot_ansible.compose_dir}"'
    for compose_file in context.nautobot_ansible.compose_files:
        compose_file_path = os.path.join(context.nautobot_ansible.compose_dir, compose_file)
        compose_command += f' -f "{compose_file_path}"'
    compose_command += f" {command}"
    print(f'Running docker compose command "{command}"')
    return context.run(compose_command, env=build_env, **kwargs)


def run_command(context, command, **kwargs):
    """Wrapper to run a command locally or inside the nautobot container."""
    if is_truthy(context.nautobot_ansible.local):
        context.run(command, **kwargs)
    else:
        # Check if netbox is running, no need to start another netbox container to run a command
        docker_compose_status = "ps --services --filter status=running"
        results = docker_compose(context, docker_compose_status, hide="out")
        if "nautobot" in results.stdout:
            compose_command = f"exec nautobot {command}"
        else:
            compose_command = f"run --entrypoint '{command}' nautobot"

        docker_compose(context, compose_command, pty=True)


# ------------------------------------------------------------------------------
# BUILD
# ------------------------------------------------------------------------------
@task(
    help={
        "force_rm": "Always remove intermediate containers",
        "cache": "Whether to use Docker's cache when building the image (defaults to enabled)",
    }
)
def build(context, force_rm=False, cache=True):
    """Build Nautobot docker image."""
    command = "build"

    if not cache:
        command += " --no-cache"
    if force_rm:
        command += " --force-rm"

    print(f"Building Nautobot with Python {context.nautobot_ansible.python_ver}...")
    print(f"Nautobot Version: {context.nautobot_ansible.nautobot_ver}")
    docker_compose(context, command)


# ------------------------------------------------------------------------------
# START / STOP / DEBUG
# ------------------------------------------------------------------------------
@task
def debug(context):
    """Start Nautobot and its dependencies in debug mode."""
    print("Starting Nautobot in debug mode...")
    docker_compose(context, "up")


@task
def start(context):
    """Start Nautobot and its dependencies in detached mode."""
    print("Starting Nautobot in detached mode...")
    docker_compose(context, "up --detach")


@task
def restart(context):
    """Gracefully restart all containers."""
    print("Restarting Nautobot...")
    docker_compose(context, "restart")


@task
def stop(context):
    """Stop Nautobot and its dependencies."""
    print("Stopping Nautobot...")
    docker_compose(context, "down")


@task
def destroy(context):
    """Destroy all containers and volumes."""
    print("Destroying Nautobot...")
    docker_compose(context, "down --volumes --remove-orphans")


# ------------------------------------------------------------------------------
# ACTIONS
# ------------------------------------------------------------------------------
@task
def nbshell(context):
    """Launch an interactive nbshell session."""
    command = "nautobot-server nbshell"
    run_command(context, command)


@task
def cli(context):
    """Launch a bash shell inside the running Nautobot container."""
    run_command(context, "bash")


@task(help={"user": "name of the superuser to create (default: admin)"})
def createsuperuser(context, user="admin"):
    """Create a new Nautobot superuser account (default: "admin"), will prompt for password."""
    command = f"nautobot-server createsuperuser --username {user}"

    run_command(context, command)


@task(help={"name": "name of the migration to be created; if unspecified, will autogenerate a name"})
def makemigrations(context, name=""):
    """Perform makemigrations operation in Django."""
    command = "nautobot-server makemigrations my_plugin"

    if name:
        command += f" --name {name}"

    run_command(context, command)


@task
def migrate(context):
    """Perform migrate operation in Django."""
    command = "nautobot-server migrate"

    run_command(context, command)


@task(help={})
def post_upgrade(context):
    """Performs Nautobot common post-upgrade operations using a single entrypoint.

    This will run the following management commands with default settings, in order:
    - migrate
    - trace_paths
    - collectstatic
    - remove_stale_contenttypes
    - clearsessions
    - invalidate all
    """
    command = "nautobot-server post_upgrade"

    run_command(context, command)


# ------------------------------------------------------------------------------
# TESTING
# ------------------------------------------------------------------------------
@task
def lint(context):
    """Run linting tools."""
    context.run(
        f"docker compose --project-name {context.nautobot_ansible.project_name} up --build --force-recreate --exit-code-from lint lint",
        env={"PYTHON_VER": context.nautobot_ansible.python_ver},
    )


@task(
    help={
        "verbose": "Run the tests with verbose output; can be provided multiple times for more verbosity (e.g. -v, -vv, -vvv)",
        "skip": "Skip specific tests (choices: lint, sanity, unit); can be provided multiple times (e.g. --skip lint --skip sanity)",
    },
    iterable=["skip"],
    incrementable=["verbose"],
)
def unit(context, verbose=0, skip=None):
    """Run unit tests."""
    env = {"PYTHON_VER": context.nautobot_ansible.python_ver}
    if verbose:
        env["ANSIBLE_SANITY_ARGS"] = f"-{'v' * verbose}"
        env["ANSIBLE_UNIT_ARGS"] = f"-{'v' * verbose}"
    if skip is not None:
        if "lint" in skip:
            env["SKIP_LINT_TESTS"] = "true"
        if "sanity" in skip:
            env["SKIP_SANITY_TESTS"] = "true"
        if "unit" in skip:
            env["SKIP_UNIT_TESTS"] = "true"
    context.run(
        f"docker compose --project-name {context.nautobot_ansible.project_name} up --build --force-recreate --exit-code-from unit unit",
        env=env,
    )
    # Clean up after the tests
    context.run(f"docker compose --project-name {context.nautobot_ansible.project_name} down")


@task(
    help={
        "verbose": "Run the tests with verbose output; can be provided multiple times for more verbosity (e.g. -v, -vv, -vvv)",
        "tags": "Run specific test tags (e.g. 'device' or 'location'); can be provided multiple times (e.g. --tags device --tags location)",
        "update_inventories": "Update the inventory integration test JSON files with the latest data",
        "skip": "Skip specific tests (choices: lint, sanity, unit, inventory, regression); can be provided multiple times (e.g. --skip lint --skip sanity)",
    },
    iterable=["tags", "skip"],
    incrementable=["verbose"],
)
def integration(context, verbose=0, tags=None, update_inventories=False, skip=None):
    """Run all tests including integration tests."""
    build(context)
    # Destroy any existing containers and volumes that may be left over from a previous run
    destroy(context)
    start(context)
    env = {
        "PYTHON_VER": context.nautobot_ansible.python_ver,
        "NAUTOBOT_VER": context.nautobot_ansible.nautobot_ver,
    }
    ansible_args = []
    if verbose:
        ansible_args.append(f"-{'v' * verbose}")
    if tags:
        ansible_args.append(f"--tags {','.join(tags)}")
    if ansible_args:
        env["ANSIBLE_INTEGRATION_ARGS"] = " ".join(ansible_args)
    if update_inventories:
        env["OUTPUT_INVENTORY_JSON"] = "/tmp/inventory_files"  # noqa: S108
    if skip is not None:
        if "lint" in skip:
            env["SKIP_LINT_TESTS"] = "true"
        if "sanity" in skip:
            env["SKIP_SANITY_TESTS"] = "true"
        if "unit" in skip:
            env["SKIP_UNIT_TESTS"] = "true"
        if "inventory" in skip:
            env["SKIP_INVENTORY_TESTS"] = "true"
        if "regression" in skip:
            env["SKIP_REGRESSION_TESTS"] = "true"
    context.run(
        f"docker compose --project-name {context.nautobot_ansible.project_name} up --build --force-recreate --exit-code-from integration integration",
        env=env,
    )
    # Clean up after the tests
    destroy(context)


@task(
    help={
        "force": "Force the build command to create a new collection, overwriting any existing files.",
    },
)
def galaxy_build(context, force=False):
    """Build the collection."""
    command = "ansible-galaxy collection build ."
    if force:
        command += " --force"
    context.run(command)


@task(
    help={
        "force": "Force the install command to update the destination folder, replacing any existing files.",
    },
)
def galaxy_install(context, force=False):
    """Install the collection to ./collections."""
    command = "ansible-galaxy collection install . -p ./collections"
    if force:
        command += " --force"
    context.run(command)


# ------------------------------------------------------------------------------
# DOCS
# ------------------------------------------------------------------------------
@task
def docs(context):
    """Build and serve docs locally for development."""
    galaxy_install(context, force=True)
    command = "poetry run mkdocs serve -v -a 0.0.0.0:8000"
    context.run(command)


@task(
    help={
        "version": "Version of nautobot-ansible to generate the release notes for.",
    }
)
def generate_release_notes(context, version=""):
    """Generate Release Notes using Towncrier."""
    command = "poetry run towncrier build"
    if version:
        command += f" --version {version}"
    else:
        command += " --version `poetry version -s`"
    # Due to issues with git repo ownership in the containers, this must always run locally.
    context.run(command)


@task
def check_versions(_):
    """Check that galaxy.yml and pyproject.toml versions match."""
    # In CI, we use invoke to install the dependencies so we need to import toml and yaml here
    import toml  # pylint: disable=import-outside-toplevel
    import yaml  # pylint: disable=import-outside-toplevel

    # Read galaxy.yml version
    with open("galaxy.yml", encoding="utf-8") as f:
        galaxy_data = yaml.safe_load(f)
        galaxy_version = galaxy_data["version"]

    # Read pyproject.toml version
    with open("pyproject.toml", encoding="utf-8") as f:
        pyproject_data = toml.load(f)
        pyproject_version = pyproject_data["tool"]["poetry"]["version"]

    if galaxy_version != pyproject_version:
        raise Exit(
            f"Version mismatch: galaxy.yml ({galaxy_version}) != pyproject.toml ({pyproject_version})",
            code=1,
        )
    print(f"Galaxy.yml and pyproject.toml versions match: {galaxy_version}")

    # Read changelogs/changelog.yaml
    with open("changelogs/changelog.yaml", encoding="utf-8") as f:
        changelog_data = yaml.safe_load(f)
        # Check if the pyproject.toml version is in the changelog
        changelog_version = changelog_data["releases"].get(pyproject_version, None)

    if changelog_version is None:
        raise Exit(
            f"Version {pyproject_version} missing from changelogs/changelog.yaml",
            code=1,
        )
    print(f"Changelogs/changelog.yaml version found: {pyproject_version}")


@task(aliases=("a",))
def autoformat(context):
    """Run code autoformatting."""
    ruff(context, action=["format"], fix=True)


@task(
    help={
        "action": "Available values are `['lint', 'format']`. Can be used multiple times. (default: `['lint', 'format']`)",
        "target": "File or directory to inspect, repeatable (default: all files in the project will be inspected)",
        "fix": "Automatically fix selected actions. May not be able to fix all issues found. (default: False)",
        "output_format": "See https://docs.astral.sh/ruff/settings/#output-format for details. (default: `concise`)",
    },
    iterable=["action", "target"],
)
def ruff(context, action=None, target=None, fix=False, output_format="concise"):
    """Run ruff to perform code formatting and/or linting."""
    if not action:
        action = ["lint", "format"]
    if not target:
        target = ["."]

    exit_code = 0

    if "format" in action:
        command = "ruff format "
        if not fix:
            command += "--check "
        command += " ".join(target)
        if not context.run(command, warn=True):
            exit_code = 1

    if "lint" in action:
        command = "ruff check "
        if fix:
            command += "--fix "
        command += f"--output-format {output_format} "
        command += " ".join(target)
        if not context.run(command, warn=True):
            exit_code = 1

    if exit_code != 0:
        raise Exit(code=exit_code)
