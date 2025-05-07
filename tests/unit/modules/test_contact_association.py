import json
import unittest
from unittest.mock import patch
from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes

try:
    from ansible_collections.networktocode.nautobot.plugins.modules import contact_association
except ImportError:
    import sys

    sys.path.append("plugins/modules")
    import contact_association


def set_module_args(args):
    args = json.dumps({"ANSIBLE_MODULE_ARGS": args})
    basic._ANSIBLE_ARGS = to_bytes(args)


class AnsibleExitJson(Exception):
    pass


class AnsibleFailJson(Exception):
    pass


def exit_json(*args, **kwargs):
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    kwargs["failed"] = True
    raise AnsibleFailJson(kwargs)


class TestContactAssociationModule(unittest.TestCase):
    def setUp(self):
        self.mock_module_helper = patch.multiple(
            basic.AnsibleModule,
            exit_json=exit_json,
            fail_json=fail_json,
        )
        self.mock_module_helper.start()
        self.addCleanup(self.mock_module_helper.stop)

    def test_module_fails_when_required_args_missing(self):
        with self.assertRaises(AnsibleFailJson):
            set_module_args({})
            contact_association.main()

    def test_create_contact_association(self):
        args = {
            "url": "http://nautobot.local",
            "token": "token",
            "contact": {"id": "contact-uuid"},
            "object_type": "dcim.device",
            "object_id": "device-uuid",
            "role": "technical",
            "state": "present",
        }
        set_module_args(args)
        with patch("ansible_collections.networktocode.nautobot.plugins.module_utils.extras.NautobotExtrasModule.run") as mock_run:
            mock_run.return_value = None
            with self.assertRaises(AnsibleExitJson):
                contact_association.main()
            mock_run.assert_called_once()

    def test_remove_contact_association(self):
        args = {
            "url": "http://nautobot.local",
            "token": "token",
            "contact": {"id": "contact-uuid"},
            "object_type": "dcim.device",
            "object_id": "device-uuid",
            "state": "absent",
        }
        set_module_args(args)
        with patch("ansible_collections.networktocode.nautobot.plugins.module_utils.extras.NautobotExtrasModule.run") as mock_run:
            mock_run.return_value = None
            with self.assertRaises(AnsibleExitJson):
                contact_association.main()
            mock_run.assert_called_once()
