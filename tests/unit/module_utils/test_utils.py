"""Tests for module_utils functions."""

from typing import Any

import pytest

try:
    from plugins.module_utils.utils import is_truthy, check_needs_wrapping
except ImportError:
    import sys

    sys.path.append("plugins/module_utils")
    sys.path.append("tests")
    from utils import is_truthy


@pytest.mark.parametrize(
    "value, expected",
    [
        (True, True),
        (False, False),
        ("true", True),
        ("false", False),
        ("True", True),
        ("False", False),
        ("TRUE", True),
        ("FALSE", False),
        ("t", True),
        ("f", False),
        ("T", True),
        ("F", False),
        ("yes", True),
        ("no", False),
        ("Yes", True),
        ("No", False),
        ("YES", True),
        ("NO", False),
        ("y", True),
        ("n", False),
        ("Y", True),
        ("N", False),
        ("1", True),
        ("0", False),
    ],
)
def test_is_truthy(value: Any, expected: bool) -> None:
    assert is_truthy(value) == expected


def test_is_truthy_raises_exception_on_invalid_type() -> None:
    with pytest.raises(ValueError) as excinfo:
        is_truthy("test")

    assert "Invalid truthy value" in str(excinfo.value)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("simplestring", False),
        ("simple multi word string", False),
        ("{{stringneedswrapping}}", True),
        ("{{ stringneedswrapping }}", True),
        ("this{{ stringneedswrapping }}", True),
        ("{% this stringneedswrapping %}", True),
        ("{% this stringneedswrapping", True),
        ("this {{ stringneedswrapping", True),
        (["nojinja", "stillnojinja"], False),
        (["safe", "{{ unsafe }}"], True),
        ({"key": "nojinja"}, False),
        ({"key": "{{jinja}}"}, True),
        ({"outer": {"inner": "{%jinja%}"}}, True),
        (["nest", {"deep": ["safe", "{% unsafe %}"]}], True),
        ([], False),
        ({}, False),
    ],
)
def test_check_needs_wrapping(value: Any, expected: bool) -> None:
    assert check_needs_wrapping(value) == expected
