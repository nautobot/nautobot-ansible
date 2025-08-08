import json
import sys
import unittest
from io import BytesIO
from unittest.mock import Mock, patch

from ansible.module_utils import basic
from parameterized import parameterized

try:
    from ansible_collections.networktocode.nautobot.plugins.modules import nautobot_server

    MOCKER_PATCH_PATH = "ansible_collections.networktocode.nautobot.plugins.modules.nautobot_server"
except ImportError:
    # Not installed as a collection
    # Try importing relative to root directory of this ansible_modules project
    sys.path.append("tests")
    sys.path.append("plugins/modules")
    MOCKER_PATCH_PATH = "plugins.modules.nautobot_server"

    import nautobot_server


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""

    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""

    pass


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs["failed"] = True
    raise AnsibleFailJson(kwargs)


def get_bin_path(self, arg, required=False):
    """Mock AnsibleModule.get_bin_path"""
    if arg.endswith("my_command"):
        return "/usr/bin/my_command"
    else:
        if required:
            fail_json(msg="%r not found !" % arg)


class TestNautobotServer(unittest.TestCase):
    def setUp(self):
        self.mock_module_helper = patch.multiple(
            basic.AnsibleModule,
            exit_json=exit_json,
            fail_json=fail_json,
            get_bin_path=get_bin_path,
        )
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fail_when_required_args_missing(self):
        args = json.dumps({"ANSIBLE_MODULE_ARGS": {}})
        mock_stdin = Mock()
        mock_stdin.buffer = BytesIO(args.encode("utf-8"))
        with self.assertRaises(AnsibleFailJson):
            with patch.object(sys, "stdin", mock_stdin):
                nautobot_server.main()

    @parameterized.expand(
        [
            [
                {
                    "command": "createsuperuser",
                    "args": {"username": "admin", "email": "admin@example.com"},
                    "db_password": "secret_password",
                    "project_path": "/some/other",
                },
                AnsibleExitJson,
                "Superuser created successfully",
                True,
                ["nautobot-server createsuperuser --noinput --username=admin --email=admin@example.com"],
                {
                    "cwd": "/some/other",
                    "environ_update": {"NAUTOBOT_ROOT": "/some/other", "NAUTOBOT_DB_PASSWORD": "secret_password"},
                },
            ],
            [
                {
                    "command": "createsuperuser",
                    "args": {"username": "admin", "email": "admin@example.com"},
                    "db_password": "secret_password",
                },
                AnsibleExitJson,
                "Superuser created successfully",
                True,
                ["nautobot-server createsuperuser --noinput --username=admin --email=admin@example.com"],
                {
                    "cwd": "/opt/nautobot",
                    "environ_update": {"NAUTOBOT_ROOT": "/opt/nautobot", "NAUTOBOT_DB_PASSWORD": "secret_password"},
                },
            ],
            [
                {
                    "command": "createsuperuser",
                    "args": {"username": "admin", "email": "admin@example.com"},
                    "db_password": "secret_password",
                },
                AnsibleExitJson,
                "username is already taken",
                False,
                ["nautobot-server createsuperuser --noinput --username=admin --email=admin@example.com"],
                {
                    "cwd": "/opt/nautobot",
                    "environ_update": {"NAUTOBOT_ROOT": "/opt/nautobot", "NAUTOBOT_DB_PASSWORD": "secret_password"},
                },
            ],
            [
                {"command": "migrate", "db_password": "secret_password"},
                AnsibleExitJson,
                "Migrating forwards ",
                True,
                ["nautobot-server migrate --noinput"],
                {
                    "cwd": "/opt/nautobot",
                    "environ_update": {"NAUTOBOT_ROOT": "/opt/nautobot", "NAUTOBOT_DB_PASSWORD": "secret_password"},
                },
            ],
            [
                {
                    "command": "migrate",
                    "db_password": "secret_password",
                    "flags": ["merge"],
                    "positional_args": ["my_plugin_name"],
                },
                AnsibleExitJson,
                "Migrating forwards ",
                True,
                ["nautobot-server migrate --noinput --merge my_plugin_name"],
                {
                    "cwd": "/opt/nautobot",
                    "environ_update": {"NAUTOBOT_ROOT": "/opt/nautobot", "NAUTOBOT_DB_PASSWORD": "secret_password"},
                },
            ],
            [
                {"command": "migrate", "db_password": "secret_password"},
                AnsibleExitJson,
                "No migrations to apply",
                False,
                ["nautobot-server migrate --noinput"],
                {
                    "cwd": "/opt/nautobot",
                    "environ_update": {"NAUTOBOT_ROOT": "/opt/nautobot", "NAUTOBOT_DB_PASSWORD": "secret_password"},
                },
            ],
            [
                {"command": "makemigrations", "db_password": "secret_password"},
                AnsibleExitJson,
                "Alter field",
                True,
                ["nautobot-server makemigrations --noinput"],
                {
                    "cwd": "/opt/nautobot",
                    "environ_update": {"NAUTOBOT_ROOT": "/opt/nautobot", "NAUTOBOT_DB_PASSWORD": "secret_password"},
                },
            ],
            [
                {"command": "makemigrations", "db_password": "secret_password"},
                AnsibleExitJson,
                "",
                False,
                ["nautobot-server makemigrations --noinput"],
                {
                    "cwd": "/opt/nautobot",
                    "environ_update": {"NAUTOBOT_ROOT": "/opt/nautobot", "NAUTOBOT_DB_PASSWORD": "secret_password"},
                },
            ],
            [
                {"command": "makemigrations", "db_password": "secret_password", "positional_args": ["my_plugin_name"]},
                AnsibleExitJson,
                "",
                False,
                ["nautobot-server makemigrations --noinput my_plugin_name"],
                {
                    "cwd": "/opt/nautobot",
                    "environ_update": {"NAUTOBOT_ROOT": "/opt/nautobot", "NAUTOBOT_DB_PASSWORD": "secret_password"},
                },
            ],
            [
                {"command": "collectstatic", "db_password": "secret_password"},
                AnsibleExitJson,
                "972 static files copied",
                True,
                ["nautobot-server collectstatic --noinput"],
                {
                    "cwd": "/opt/nautobot",
                    "environ_update": {"NAUTOBOT_ROOT": "/opt/nautobot", "NAUTOBOT_DB_PASSWORD": "secret_password"},
                },
            ],
            [
                {"command": "post_upgrade", "db_password": "secret_password"},
                AnsibleExitJson,
                "",
                True,
                ["nautobot-server post_upgrade"],
                {
                    "cwd": "/opt/nautobot",
                    "environ_update": {"NAUTOBOT_ROOT": "/opt/nautobot", "NAUTOBOT_DB_PASSWORD": "secret_password"},
                },
            ],
        ]
    )
    def test_ensure_command_called(self, module_args, expected_exception, stdout, changed, args, kwargs):
        json_args_string = json.dumps({"ANSIBLE_MODULE_ARGS": module_args})
        mock_stdin = Mock()
        mock_stdin.buffer = BytesIO(json_args_string.encode("utf-8"))

        with patch.object(sys, "stdin", mock_stdin):
            with patch.object(basic.AnsibleModule, "run_command") as mock_run_command:
                stderr = ""
                rc = 0
                mock_run_command.return_value = rc, stdout, stderr  # successful execution

                with self.assertRaises(expected_exception) as result:
                    nautobot_server.main()

                if expected_exception == AnsibleFailJson:
                    return

                self.assertEqual(result.exception.args[0]["changed"], changed)  # ensure result is changed

                self.assertEqual(mock_run_command.call_count, 1)
                mock_run_command.assert_called_with(*args, **kwargs)
