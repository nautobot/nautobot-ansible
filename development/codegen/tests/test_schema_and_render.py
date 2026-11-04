"""Tests for reading the API schema (schema.py) and writing YAML and Python (render.py)."""

import pytest
import yaml

from development.codegen import render, schema


def test_parse_endpoints_keeps_only_writable_fields(api):
    endpoints = schema.parse_endpoints(*api)
    cable = endpoints["/dcim/cables/"]

    assert cable.app == "dcim"
    assert cable.endpoint == "cables"
    assert cable.model == "dcim.cable"
    assert cable.creatable is True
    assert cable.tags_supported is True
    # id, display (read-only) and tags (shared argument spec) are left out.
    assert list(cable.fields) == ["label", "type", "status"]
    assert cable.fields["status"].related_model == "extras.status"
    assert cable.fields["status"].required is True
    assert cable.fields["type"].choices == ["cat5", "cat6"]
    assert cable.fields["type"].choice_labels == ["CAT5", "CAT6"]


def test_parse_endpoints_keeps_endpoints_without_post(api):
    schema_data, metadata = api
    del schema_data["paths"]["/extras/statuses/"]["post"]

    endpoints = schema.parse_endpoints(schema_data, metadata)

    assert endpoints["/extras/statuses/"].creatable is False
    assert endpoints["/extras/statuses/"].fields == {}


def test_parse_endpoints_reads_bulk_request_bodies(api):
    """Bulk-capable endpoints describe the body as one object or a list of objects."""
    schema_data, metadata = api
    body = schema_data["paths"]["/dcim/cable-types/"]["post"]["requestBody"]["content"]["application/json"]
    body["schema"] = {
        "oneOf": [
            {"$ref": "#/components/schemas/CabletypeRequest"},
            {"type": "array", "items": {"$ref": "#/components/schemas/CabletypeRequest"}},
        ]
    }

    endpoints = schema.parse_endpoints(schema_data, metadata)

    assert list(endpoints["/dcim/cable-types/"].fields) == ["name", "total_lanes"]


def test_extract_metadata_json_ignores_other_output():
    output = f'199 objects imported automatically\n{schema.BEGIN_MARKER}\n{{"models": {{}}}}\n{schema.END_MARKER}\n'
    assert schema.extract_metadata_json(output) == '{"models": {}}'


def test_extract_metadata_json_without_markers_fails():
    with pytest.raises(ValueError):
        schema.extract_metadata_json("Traceback (most recent call last): ...")


def test_to_yaml_matches_the_module_documentation_style():
    text = render.to_yaml(
        {"version_added": "3.0.0", "description": ["First line", "Second line"], "removed_in": "7.0.0"}
    )
    assert text == ('version_added: "3.0.0"\ndescription:\n  - First line\n  - Second line\nremoved_in: "7.0.0"\n')


def test_to_yaml_round_trips_multiline_strings_and_tuples():
    data = {"examples": "\n- name: test\n  debug:\n", "required_if": [("state", "new", ["address"], True)]}
    loaded = yaml.safe_load(render.to_yaml(data))
    assert loaded == {"examples": data["examples"], "required_if": [["state", "new", ["address"], True]]}
    assert "examples: |" in render.to_yaml(data)


def test_to_python():
    assert render.to_python({"required": False, "type": "raw"}) == 'dict(required=False, type="raw")'
    assert render.to_python({"dcim.interface": "interfaces"}) == '{"dcim.interface": "interfaces"}'
    assert render.to_python(("state", "new", ["a"], True)) == '("state", "new", ["a"], True)'
    assert render.to_python(("a",)) == '("a",)'
    assert render.to_python('say "hi"') == '"say \\"hi\\""'
    with pytest.raises(TypeError):
        render.to_python(object())
