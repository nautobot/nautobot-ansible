"""Tests for module_utils functions."""
from typing import Any

import pytest

try:
    from plugins.module_utils.utils import is_truthy
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
