"""Tests for module_utils functions."""

import json
from typing import Any

import pytest
from plugins.module_utils.utils import sort_dict_with_lists

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


@pytest.mark.parametrize(
    "data, expected",
    [
        # Simple dictionary with sorted keys
        ({"b": 2, "a": 1}, {"a": 1, "b": 2}),
        ({"z": 26, "y": 25, "x": 24}, {"x": 24, "y": 25, "z": 26}),
        # Dictionary with unsorted list values
        ({"items": [3, 1, 2], "name": "test"}, {"items": [1, 2, 3], "name": "test"}),
        ({"data": ["zebra", "apple", "banana"], "count": 3}, {"count": 3, "data": ["apple", "banana", "zebra"]}),
        # Nested dictionaries
        ({"b": {"d": 4, "c": 3}, "a": {"f": 6, "e": 5}}, {"a": {"e": 5, "f": 6}, "b": {"c": 3, "d": 4}}),
        # Lists of dictionaries
        ({"users": [{"id": 2, "name": "Bob"}, {"id": 1, "name": "Alice"}]}, {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}),
        # Mixed nested structures
        (
            {"config": {"servers": [{"port": 8080, "host": "server2"}, {"port": 80, "host": "server1"}]}},
            {"config": {"servers": [{"host": "server1", "port": 80}, {"host": "server2", "port": 8080}]}},
        ),
        # Lists with mixed types
        ({"mixed": [{"b": 2, "a": 1}, [3, 1, 2], "string", 42]}, {"mixed": ["string", 42, [1, 2, 3], {"a": 1, "b": 2}]}),
        # Deep nesting
        ({"level1": {"level2": {"level3": {"items": [3, 1, 2]}}}}, {"level1": {"level2": {"level3": {"items": [1, 2, 3]}}}}),
        # Empty structures
        ({}, {}),
        ({"empty_list": [], "empty_dict": {}}, {"empty_dict": {}, "empty_list": []}),
        # Lists of lists
        ({"matrix": [[3, 1, 2], [6, 4, 5]]}, {"matrix": [[1, 2, 3], [4, 5, 6]]}),
        # Dictionary with None values
        ({"b": None, "a": 1, "c": None}, {"a": 1, "b": None, "c": None}),
        # Dictionary with boolean values
        ({"b": False, "a": True, "c": False}, {"a": True, "b": False, "c": False}),
        # Dictionary with string values
        ({"zebra": "animal", "apple": "fruit", "banana": "fruit"}, {"apple": "fruit", "banana": "fruit", "zebra": "animal"}),
        # Complex nested structure
        (
            {"api": {"endpoints": [{"methods": ["POST", "GET"], "path": "/users"}, {"methods": ["PUT", "DELETE"], "path": "/items"}]}, "version": "1.0"},
            {"api": {"endpoints": [{"methods": ["DELETE", "PUT"], "path": "/items"}, {"methods": ["GET", "POST"], "path": "/users"}]}, "version": "1.0"},
        ),
    ],
)
def test_sort_dict_with_lists(data: Any, expected: Any) -> None:
    """Test sort_dict_with_lists with various data structures."""
    result = sort_dict_with_lists(data)
    assert result == expected


def test_sort_dict_with_lists_non_dict_inputs() -> None:
    """Test sort_dict_with_lists with non-dictionary inputs."""
    # Test with list input
    assert sort_dict_with_lists([3, 1, 2]) == [1, 2, 3]
    assert sort_dict_with_lists([{"b": 2, "a": 1}, {"d": 4, "c": 3}]) == [{"a": 1, "b": 2}, {"c": 3, "d": 4}]

    # Test with primitive types
    assert sort_dict_with_lists(42) == 42
    assert sort_dict_with_lists("hello") == "hello"
    assert sort_dict_with_lists(True) is True
    assert sort_dict_with_lists(None) is None


def test_sort_dict_with_lists_comparison_consistency() -> None:
    """Test that sort_dict_with_lists produces consistent results for comparison."""
    # Two dictionaries that should be equal after sorting
    dict1 = {"b": {"d": 4, "c": 3}, "a": [3, 1, 2]}
    dict2 = {"a": [1, 2, 3], "b": {"c": 3, "d": 4}}

    # They should be different before sorting
    assert dict1 != dict2

    # They should be equal after sorting
    assert sort_dict_with_lists(dict1) == sort_dict_with_lists(dict2)


def test_sort_dict_with_lists_edge_cases() -> None:
    """Test sort_dict_with_lists with edge cases."""
    # Single item structures
    assert sort_dict_with_lists({"a": 1}) == {"a": 1}
    assert sort_dict_with_lists([1]) == [1]

    # Structures with duplicate values
    assert sort_dict_with_lists({"items": [1, 1, 2, 2, 3]}) == {"items": [1, 1, 2, 2, 3]}

    # Mixed data types in lists
    assert sort_dict_with_lists({"data": [3, "a", 1, "b", 2]}) == {"data": ["a", "b", 1, 2, 3]}

    # Unicode strings
    assert sort_dict_with_lists({"items": ["café", "apple", "banana"]}) == {"items": ["apple", "banana", "café"]}


def test_sort_dict_with_lists_nested_empty_structures() -> None:
    """Test sort_dict_with_lists with nested empty structures."""
    data = {"empty_dict": {}, "empty_list": [], "nested_empty": {"inner_dict": {}, "inner_list": []}, "mixed_empty": {"dict": {}, "list": [], "value": 42}}

    expected = {"empty_dict": {}, "empty_list": [], "mixed_empty": {"dict": {}, "list": [], "value": 42}, "nested_empty": {"inner_dict": {}, "inner_list": []}}

    assert sort_dict_with_lists(data) == expected


def test_regression_issue_568() -> None:
    """Test dict from issue #568."""
    with open("tests/unit/module_utils/test_data/regression_tests/issue_568.json", "r", encoding="utf-8") as f:
        jason = json.load(f)
        data = jason["data"]
        expected = jason["expected"]

    assert sort_dict_with_lists(data) == expected
