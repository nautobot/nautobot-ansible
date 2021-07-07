import json

import unittest
from unittest.mock import patch
from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes

try:
    from plugins.modules import nautobot_server
except ImportError:
    import sys

    sys.path.append("tests")
    sys.path.append("plugins/modules")

    import nautobot_server


def set_module_args(args):
    """prepare arguments so that they will be picked up during module creation"""
    args = json.dumps({"ANSIBLE_MODULE_ARGS": args})
    basic._ANSIBLE_ARGS = to_bytes(args)


class AnsibleExitJson(Exception):
    """Exception class to be raised by module.exit_json and caught by the test case"""

    pass


class AnsibleFailJson(Exception):
    """Exception class to be raised by module.fail_json and caught by the test case"""

    pass


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    if "changed" not in kwargs:
        kwargs["changed"] = False
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
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            nautobot_server.main()

    def test_ensure_command_called(self):
        set_module_args(
            {
                "command": "createsuperuser --noinput --username=admin --email=admin@example.com",
                "project_path": "/some/path",
            }
        )

        with patch.object(basic.AnsibleModule, "run_command") as mock_run_command:
            stdout = "configuration updated"
            stderr = ""
            rc = 0
            mock_run_command.return_value = rc, stdout, stderr  # successful execution

            with self.assertRaises(AnsibleExitJson) as result:
                nautobot_server.main()
            self.assertFalse(
                result.exception.args[0]["changed"]
            )  # ensure result is changed

        self.assertEqual(mock_run_command.call_count, 2)

        args = [
            "nautobot-server createsuperuser --noinput --username=admin --email=admin@example.com"
        ]
        kwargs = {
            "cwd": "/some/path",
            "environ_update": {"NAUTOBOT_ROOT": "/some/path"},
        }
        mock_run_command.assert_called_with(*args, **kwargs)
