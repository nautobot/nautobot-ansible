"""Load an Ansible module file and capture what it passes to AnsibleModule.

Used by the bootstrap script, the tests, and `compare.py` to read a module's real `argument_spec`
(and other AnsibleModule keyword arguments) without connecting to Nautobot.
"""

import importlib
import importlib.util
import os
import sys
import tempfile
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
COLLECTION_PACKAGE = "ansible_collections.networktocode.nautobot"


class _Captured(Exception):
    """Raised by the stub AnsibleModule to stop the module after it has been constructed."""

    def __init__(self, kwargs):
        super().__init__("captured")
        self.kwargs = kwargs


class _StubAnsibleModule:
    def __init__(self, **kwargs):
        raise _Captured(kwargs)


_COLLECTION_ROOT = {}


def ensure_collection_importable():
    """Make `ansible_collections.networktocode.nautobot` importable from this checkout.

    The repository isn't laid out as `ansible_collections/networktocode/nautobot`, so this creates that
    layout with a symlink in a temporary directory and adds it to `sys.path`.
    """
    if "path" in _COLLECTION_ROOT:
        return _COLLECTION_ROOT["path"]
    root = tempfile.mkdtemp(prefix="nautobot-ansible-codegen-")
    namespace_dir = Path(root, "ansible_collections", "networktocode")
    namespace_dir.mkdir(parents=True)
    os.symlink(REPO_ROOT, namespace_dir / "nautobot")
    sys.path.insert(0, root)
    _COLLECTION_ROOT["path"] = root
    return root


def load_module_source(source, name="module_under_test"):
    """Execute module source code and return a dict describing it.

    Returns:
        (dict): `documentation` (parsed YAML), `examples` and `return` (raw strings), and `ansible_module_kwargs`
            (the keyword arguments passed to AnsibleModule, or None if `main()` never constructed one).
    """
    ensure_collection_importable()
    import ansible.module_utils.basic  # pylint: disable=import-outside-toplevel

    spec = importlib.util.spec_from_loader(f"{COLLECTION_PACKAGE}.plugins.modules.{name}", loader=None)
    module = importlib.util.module_from_spec(spec)
    exec(compile(source, f"{name}.py", "exec"), module.__dict__)  # noqa: S102  # pylint: disable=exec-used

    result = {
        "documentation": yaml.safe_load(module.DOCUMENTATION),
        "examples": module.EXAMPLES,
        "return": module.RETURN,
        "ansible_module_kwargs": None,
    }
    if hasattr(module, "AnsibleModule"):
        original = ansible.module_utils.basic.AnsibleModule
        module.AnsibleModule = _StubAnsibleModule
        try:
            module.main()
        except _Captured as captured:
            result["ansible_module_kwargs"] = captured.kwargs
        finally:
            module.AnsibleModule = original
    return result


def load_module_file(path):
    """Load a module from a file path. See `load_module_source`."""
    path = Path(path)
    return load_module_source(path.read_text(encoding="utf-8"), name=path.stem)
