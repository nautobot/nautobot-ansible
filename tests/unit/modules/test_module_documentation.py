"""Tests to validate all modules have required Ansible documentation blocks.

Per the Ansible collection requirements:
https://docs.ansible.com/ansible/devel/community/collection_contributors/collection_requirements.html#documentation-requirements

All modules and plugins:
- MUST include a DOCUMENTATION block.
- MUST include an EXAMPLES block (except where not relevant for the plugin type).
- MUST include a RETURN block for modules and other plugins that return data.
"""

import os

import pytest

MODULES_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "plugins", "modules")
MODULES_PATH = os.path.normpath(MODULES_PATH)


def get_module_files():
    """Return a list of all Python module files (excluding __init__.py)."""
    module_files = []
    for filename in sorted(os.listdir(MODULES_PATH)):
        if filename.endswith(".py") and filename != "__init__.py":
            module_files.append(filename)
    return module_files


@pytest.mark.parametrize("module_file", get_module_files())
def test_module_has_documentation_block(module_file):
    """Every module MUST include a DOCUMENTATION block."""
    filepath = os.path.join(MODULES_PATH, module_file)
    with open(filepath, "r") as f:
        content = f.read()
    assert "DOCUMENTATION" in content, f"{module_file} is missing a DOCUMENTATION block"


@pytest.mark.parametrize("module_file", get_module_files())
def test_module_has_examples_block(module_file):
    """Every module MUST include an EXAMPLES block."""
    filepath = os.path.join(MODULES_PATH, module_file)
    with open(filepath, "r") as f:
        content = f.read()
    assert "EXAMPLES" in content, f"{module_file} is missing an EXAMPLES block"


@pytest.mark.parametrize("module_file", get_module_files())
def test_module_has_return_block(module_file):
    """Every module MUST include a RETURN block."""
    filepath = os.path.join(MODULES_PATH, module_file)
    with open(filepath, "r") as f:
        content = f.read()
    assert "RETURN" in content, f"{module_file} is missing a RETURN block"


@pytest.mark.parametrize("module_file", get_module_files())
def test_module_has_version_added(module_file):
    """Every module MUST include a version_added field in DOCUMENTATION."""
    filepath = os.path.join(MODULES_PATH, module_file)
    with open(filepath, "r") as f:
        content = f.read()
    assert "version_added" in content, f"{module_file} is missing version_added in DOCUMENTATION"
