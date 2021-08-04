#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2021, Network to Code <opensource@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: nautobot_server
short_description: Manages Nautobot Server application.
description:
    - Manages Nautobot Server using the C(nautobot-server) application frontend to C(django-admin). With the
      C(virtualenv) parameter, all management commands will be executed by the given C(virtualenv) installation.
requirements:
  - nautobot
author:
  - Network to Code (@networktocode)
options:
  command:
    description:
      - The name of the Nautobot management command to run. Some built in commands are C(collectstatic),
        C(flush), C(loaddata), C(migrate), C(test), and C(validate).
      - Other commands can be entered, but will fail if they're unknown to Nautobot. Other commands that may
        prompt for user input should be run with the C(--noinput) flag.
      - The module will perform some basic parameter validation (when applicable) to the commands C(collectstatic),
        C(createcachetable), C(flush), C(loaddata), C(migrate), C(test), and C(validate).
    type: str
    required: true
  project_path:
    description:
      - The path to the root of the Nautobot application where B(nautobot-server) lives.
    type: path
    required: false
    aliases: [app_path, chdir]
    default: /opt/nautobot
  pythonpath:
    description:
      - A directory to add to the Python path. Typically used to include the settings module if it is located
        external to the application directory.
    type: path
    required: false
    aliases: [python_path]
  virtualenv:
    description:
      - An optional path to a I(virtualenv) installation to use while running the nautobot-server application.
    type: path
    aliases: [virtual_env]
  db_password:
    description:
      - Database password used in Nautobot.
    type: str
    required: false
  apps:
    description:
      - A list of space-delimited apps/plugins to target. Used by the C(test) command.
    type: str
    required: false
  cache_table:
    description:
      - The name of the table used for database-backed caching. Used by the C(createcachetable) command.
    type: str
    required: false
  clear:
    description:
      - Clear the existing files before trying to copy or link the original file.
      - Used only with the 'collectstatic' command. The C(--noinput) argument will be added automatically.
    required: false
    default: no
    type: bool
  database:
    description:
      - The database to target. Used by the C(createcachetable), C(flush), C(loaddata) and C(migrate) commands.
    type: str
    required: false
  failfast:
    description:
      - Fail the command immediately if a test fails. Used by the C(test) command.
    required: false
    default: false
    type: bool
    aliases: [fail_fast]
  fixtures:
    description:
      - A space-delimited list of fixture file names to load in the database. B(Required) by the C(loaddata) command.
    type: str
    required: false
  skip:
    description:
     - Will skip over out-of-order missing migrations, you can only use this parameter with C(migrate) command.
    required: false
    type: bool
  merge:
    description:
     - Will run out-of-order or missing migrations as they are not rollback migrations, you can only use this
       parameter with C(migrate) command.
    required: false
    type: bool
  link:
    description:
     - Will create links to the files instead of copying them, you can only use this parameter with
       C(collectstatic) command.
    required: false
    type: bool
  testrunner:
    description:
      - "From the Django docs: Controls the test runner class that is used to execute tests."
      - This parameter is passed as-is to C(nautobot-server).
    type: str
    required: false
    aliases: [test_runner]
notes:
  - This module is inspired from Django_manage Ansible module (U(https://github.com/ansible-collections/community.general/blob/main/plugins/modules/web_infrastructure/django_manage.py)).
  - This module will create a virtualenv if the virtualenv parameter is specified and a virtualenv does not already
    exist at the given location.
  - This module assumes English error messages for the C(createcachetable) command to detect table existence and others,
    unfortunately.
  - To be able to use the C(collectstatic) command, you must have enabled staticfiles in your nautbot_config.py.
  - Your C(nautobot-server) application must be executable (rwxr-xr-x), and must have a valid shebang,
    i.e. C(#!/usr/bin/env python), for invoking the appropriate Python interpreter.
"""

EXAMPLES = """
- name: Create an initial superuser
  networktocode.nautobot.nautobot_server:
    command: "createsuperuser --noinput --username=admin --email=admin@example.com"
    db_password: "{{ db_password }}"
- name: Migrate
  networktocode.nautobot.nautobot_server:
    command: "migrate"
    db_password: "{{ db_password }}"
- name: Make Migrations
  networktocode.nautobot.nautobot_server:
    command: "makemigrations"
    db_password: "{{ db_password }}"
- name: Collectstatic
  networktocode.nautobot.nautobot_server:
    command: "collectstatic"
    db_password: "{{ db_password }}"
- name: Post Upgrade
  networktocode.nautobot.nautobot_server:
    command: "post_upgrade"
    db_password: "{{ db_password }}"
- name: Load the initial_data fixture into Nautobot
  networktocode.nautobot.nautobot_server:
    command: loaddata
    fixtures: "{{ initial_data }}"
    db_password: "{{ db_password }}"
- name: Run the SmokeTest test case from the main app. Useful for testing deploys
  networktocode.nautobot.nautobot_server:
    command: test
    apps: nautobot
    db_password: "{{ db_password }}"
"""

import os
import sys

from ansible.module_utils.basic import AnsibleModule


def _fail(module, cmd, out, err, **kwargs):
    """Helper function to customize output/error message."""
    msg = ""
    if out:
        msg += "stdout: %s" % (out,)
    if err:
        msg += "\n:stderr: %s" % (err,)
    module.fail_json(cmd=cmd, msg=msg, **kwargs)


def _ensure_virtualenv(module):
    """Ensure that virtualenv is available."""
    venv_param = module.params["virtualenv"]
    if venv_param is None:
        # If no custom virtualenv is defined, we assume it's in the project_path
        venv_param = module.params["project_path"]

    vbin = os.path.join(venv_param, "bin")
    activate = os.path.join(vbin, "activate")

    if not os.path.exists(activate):
      _fail(module, activate, "Virtualenv doens't exist.", f"{activate} not found.")

    os.environ["PATH"] = "%s:%s" % (vbin, os.environ["PATH"])
    os.environ["VIRTUAL_ENV"] = venv_param


### Helper functions to customize the output state ###


def createcachetable_check_changed(output):
    return "already exists" not in output


def flush_filter_output(line):
    return "Installed" in line and "Installed 0 object" not in line


def loaddata_filter_output(line):
    return "Installed" in line and "Installed 0 object" not in line


def migrate_filter_output(line):
    return (
        ("Migrating forwards " in line)
        or ("Installed" in line and "Installed 0 object" not in line)
        or ("Applying" in line)
    )


def collectstatic_filter_output(line):
    return line and "0 static files" not in line


######################################################


def main():
    command_allowed_param_map = dict(
        createcachetable=("cache_table", "database",),
        flush=("database",),
        loaddata=("database", "fixtures",),
        test=("failfast", "testrunner", "apps",),
        validate=(),
        migrate=("apps", "skip", "merge", "database",),
        collectstatic=("clear", "link",),
    )

    command_required_param_map = dict(loaddata=("fixtures",),)

    # forces --noinput on every command that needs it
    noinput_commands = (
        "flush",
        "migrate",
        "test",
        "collectstatic",
    )

    # These params are allowed for certain commands only
    specific_params = (
        "apps",
        "clear",
        "database",
        "failfast",
        "fixtures",
        "testrunner",
    )

    # These params are automatically added to the command if present
    general_params = ("pythonpath", "database")
    specific_boolean_params = ("clear", "failfast", "skip", "merge", "link")
    end_of_command_params = ("apps", "cache_table", "fixtures")

    module = AnsibleModule(
        argument_spec=dict(
            command=dict(required=True, type="str"),
            project_path=dict(
                default="/opt/nautobot", 
                required=False, 
                type="path", 
                aliases=["app_path", "chdir"]
            ),
            pythonpath=dict(
                default=None, required=False, type="path", aliases=["python_path"]
            ),
            virtualenv=dict(
                default=None, required=False, type="path", aliases=["virtual_env"]
            ),
            db_password=dict(default=None, required=False, type="str", no_log=True),
            apps=dict(default=None, required=False),
            cache_table=dict(default=None, required=False, type="str"),
            clear=dict(default=False, required=False, type="bool"),
            database=dict(default=None, required=False, type="str"),
            failfast=dict(
                default=False, required=False, type="bool", aliases=["fail_fast"]
            ),
            fixtures=dict(default=None, required=False, type="str"),
            testrunner=dict(
                default=None, required=False, type="str", aliases=["test_runner"]
            ),
            skip=dict(default=None, required=False, type="bool"),
            merge=dict(default=None, required=False, type="bool"),
            link=dict(default=None, required=False, type="bool"),
        ),
    )

    command = module.params["command"]
    project_path = module.params["project_path"]
    virtualenv = module.params["virtualenv"]

    for param in specific_params:
        value = module.params[param]
        if param in specific_boolean_params:
            value = module.boolean(value)
        if value and param not in command_allowed_param_map[command]:
            module.fail_json(
                msg="%s param is incompatible with command=%s" % (param, command)
            )

    for param in command_required_param_map.get(command, ()):
        if not module.params[param]:
            module.fail_json(
                msg="%s param is required for command=%s" % (param, command)
            )

    _ensure_virtualenv(module)

    cmd = "nautobot-server %s" % (command,)

    environ_vars = {}
    if project_path:
        environ_vars["NAUTOBOT_ROOT"] = project_path

    db_password = module.params["db_password"]
    if db_password:
        environ_vars["NAUTOBOT_DB_PASSWORD"] = db_password

    if command in noinput_commands:
        cmd = "%s --noinput" % cmd

    for param in general_params:
        if module.params[param]:
            cmd = "%s --%s=%s" % (cmd, param, module.params[param])

    for param in specific_boolean_params:
        if module.boolean(module.params[param]):
            cmd = "%s --%s" % (cmd, param)

    # these params always get tacked on the end of the command
    for param in end_of_command_params:
        if module.params[param]:
            cmd = "%s %s" % (cmd, module.params[param])

    rc, out, err = module.run_command(
        cmd, cwd=project_path, environ_update=environ_vars
    )
    if rc != 0:
        # Handling expected errors
        if command == "createcachetable" and "table" in err and "already exists" in err:
            out = "Cache Table already exists."
        elif "createsuperuser" in command and "username is already taken" in err:
            username =  cmd.split("--username=")[-1].split(" ")[0]
            out = f"{username} user already exists."
        else:
            # Customize some output messages
            if "Unknown command:" in err:
                _fail(module, cmd, err, "Unknown django command: %s" % command)
            elif "fe_sendauth: no password supplied" in err:
                _fail(
                    module,
                    cmd,
                    err,
                    "No DB password provided, you must supply 'db_password' for this command",
                )
            _fail(module, cmd, out, err, path=os.environ["PATH"], syspath=sys.path)

    # Customizing the final state depending on the output
    changed = False
    lines = out.split("\n")
    filt = globals().get(command + "_filter_output", None)
    if filt:
        filtered_output = list(filter(filt, lines))
        if len(filtered_output):
            changed = True
    check_changed = globals().get(f"{command}_check_changed", None)
    if check_changed:
        changed = check_changed(out)

    module.exit_json(
        changed=changed,
        out=out,
        cmd=cmd,
        app_path=project_path,
        project_path=project_path,
        virtualenv=virtualenv,
        pythonpath=module.params["pythonpath"],
    )


if __name__ == "__main__":
    main()
