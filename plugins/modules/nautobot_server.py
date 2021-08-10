#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2021, Network to Code <opensource@networktocode.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {
    "metadata_version": "1.0",
    "status": ["preview"],
    "supported_by": "community",
}


DOCUMENTATION = r"""
---
module: nautobot_server
short_description: Manages Nautobot Server application.
description:
    - Manages Nautobot Server using the C(nautobot-server) application frontend to C(django-admin). With the C(virtualenv) parameter, all management commands will be executed by the given C(virtualenv) installation.
requirements:
  - nautobot
author:
  - Network to Code (@networktocode)
options:
  command:
    description:
      - The name of the Nautobot management command to run. Some command fully implemented are: C(createsuperuser), C(migrate), C(makemigrations), C(post_upgrade) and C(collectstatic).
      - Other commands can be entered, but will fail if they're unknown to Nautobot or use positional arguments.
      - The module will perform some basic parameter validation (when applicable) to the commands.
    type: str
    required: true
  args:
    description:
      - A dictionary of the arguments used together with the command. Depending on the pre-defined type, the argument can be a flag, an optional argument or a positional argument. If not defined in the code, the default assumption is an optional argument, so "name_arg: value_arg" is translated to "--name_arg value_arg".
    type: dict
    required: false
  positional_args:
    description:
      - A list of additional arguments to append to the end of the command that is passed to `nautobot-server`.
      - These are appended to the end of the command, so that ["arg1", "arg2"] is translated to "arg1 arg2".
    type: list
    required: false
  flags:
    description:
      - A list of flags to append to the command that is passed to `nautobot-server`, so that ["flag1", "flag2"] is translated to "--flag1 --flag2".
    type: list
    required: false
  project_path:
    description:
      - The path to the root of the Nautobot application where B(nautobot-server) lives.
    type: path
    required: false
    aliases: [app_path, chdir]
    default: /opt/nautobot
  pythonpath:
    description:
      - A directory to add to the Python path. Typically used to include the settings module if it is located external to the application directory.
    type: path
    required: false
    aliases: [python_path]
  virtualenv:
    description:
      - An optional path to a I(virtualenv) installation to use while running the nautobot-server application.
    type: path
    required: false
    aliases: [virtual_env]
  db_password:
    description:
      - Database password used in Nautobot.
    type: str
    required: false
notes:
  - This module is inspired from Django_manage Ansible module (U(https://github.com/ansible-collections/community.general/blob/main/plugins/modules/web_infrastructure/django_manage.py)).
  - To be able to use the C(collectstatic) command, you must have enabled staticfiles in your nautbot_config.py.
  - Your C(nautobot-server) application must be executable (rwxr-xr-x), and must have a valid shebang, i.e. C(#!/usr/bin/env python), for invoking the appropriate Python interpreter.
"""

EXAMPLES = r"""
  - name: Createsuperuser
    networktocode.nautobot.nautobot_server:
      command: "createsuperuser"
      args:
        email: "admin93@example.com"
        username: "superadmin7"
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
  - name: Make Migrations for Plugin
    networktocode.nautobot.nautobot_server:
      command: "makemigrations"
      positional_args: ["my_plugin_name"]
      db_password: "{{ db_password }}"
  - name: Migrate Plugin
    networktocode.nautobot.nautobot_server:
      command: "migrate"
      args:
        verbosity: 3
      flags: ["merge"]
      positional_args: ["my_plugin_name"]
      db_password: "{{ db_password }}"
"""

RETURN = r"""
changed:
  description: Boolean that is true if the command changed the state.
  returned: always
  type: bool
  sample: True
out:
  description: Raw output from the command execution.
  returned: always
  type: string
  sample: superadmin user already exists.
cmd:
  description: Full command executed in the Server.
  returned: always
  type: string
  sample: nautobot-server createsuperuser --noinput --email=admin33@example.com --username=superadmin
project_path:
  description: The path to the root of the Nautobot application where B(nautobot-server) lives.
  returned: always
  type: path
  sample: /opt/nautobot
virtualenv:
  description: An optional path to a I(virtualenv) installation to use while running the nautobot-server application.
  returned: when defined
  type: path
  sample: /opt/nautobot/.venv
pythonpath:
  description: A directory to add to the Python path. Typically used to include the settings module if it is located external to the application directory.
  returned: when defined
  type: path
  sample: /usr/settings
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
    # If no custom virtualenv is defined, we assume it's in the project_path
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


def createsuperuser_changed(line):
    return "Superuser created successfully" in line


def migrate_changed(line):
    return (
        ("Migrating forwards " in line)
        or ("Installed" in line and "Installed 0 object" not in line)
        or ("Applying" in line)
    )


def makemigrations_changed(line):
    return (
        ("Alter field" in line)
        or ("Add field" in line)
        or ("Run Python" in line)
        or ("Rename field" in line)
        or ("Remove field" in line)
    )


def post_upgrade_changed(line):
    # post_upgrade always changes the state, even only removing state and invalidating cache.
    return True


def collectstatic_changed(line):
    return line and "0 static files" not in line


######################################################


def main():

    # Commands that are known to use the --noinput flag
    commands_with_noinput = {
        "createsuperuser",
        "migrate",
        "makemigrations",
        "collectstatic",
    }

    required_if = [
        ["command", "createsuperuser", ["args"]],
    ]

    module = AnsibleModule(
        argument_spec=dict(
            command=dict(required=True, type="str"),
            args=dict(type="dict", default={}),
            positional_args=dict(type="list", default=[]),
            flags=dict(type="list", default=[]),
            project_path=dict(
                default="/opt/nautobot",
                type="path",
                aliases=["app_path", "chdir"],
            ),
            pythonpath=dict(required=False, type="path", aliases=["python_path"]),
            virtualenv=dict(required=False, type="path", aliases=["virtual_env"]),
            db_password=dict(required=True, type="str", no_log=True),
        ),
        required_if=required_if,
    )

    command = module.params["command"]
    args = module.params["args"]
    flags = module.params["flags"]
    positional_args = module.params["positional_args"]
    project_path = module.params["project_path"]

    _ensure_virtualenv(module)

    cmd = "nautobot-server %s" % (command,)

    environ_vars = {}
    if project_path:
        environ_vars["NAUTOBOT_ROOT"] = project_path

    db_password = module.params["db_password"]
    if db_password:
        environ_vars["NAUTOBOT_DB_PASSWORD"] = db_password

    if command in commands_with_noinput:
        cmd = "%s --noinput" % cmd

    for flag in flags:
        if flag == "noinput" and command in commands_with_noinput:
            continue

        cmd += " --%s" % (flag,)

    for arg, value in args.items():
        cmd += " --%s=%s" % (arg, value)

    for value in positional_args:
        cmd += " %s" % (value,)

    rc, out, err = module.run_command(
        cmd, cwd=project_path, environ_update=environ_vars
    )
    if rc != 0:
        # Handling expected errors
        if command == "createcachetable" and "table" in err and "already exists" in err:
            out = "Cache Table already exists."
        elif "createsuperuser" in command and "username is already taken" in err:
            username = cmd.split("--username=")[-1].split(" ")[0]
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
    filt = globals().get(f"{command}_changed", None)
    if filt:
        filtered_output = list(filter(filt, lines))
        if len(filtered_output):
            changed = True

    return_kwargs = {
        "changed": changed,
        "out": out,
        "cmd": cmd,
        "project_path": project_path,
    }

    module.exit_json(**return_kwargs)


if __name__ == "__main__":
    main()
