"""Fixtures that build a small OpenAPI schema and model metadata for the code generator tests."""

import copy

import pytest

RELATED = {
    "type": "object",
    "properties": {"id": {"type": "string", "format": "uuid"}, "object_type": {"type": "string"}},
}


def field_metadata(name, **kwargs):
    data = {
        "name": name,
        "serializer_field": "CharField",
        "read_only": False,
        "write_only": False,
        "required": False,
        "allow_null": False,
        "help_text": None,
        "label": None,
        "many": False,
        "related_model": None,
        "choices": None,
        "choice_labels": None,
        "content_types": None,
        "model_help_text": None,
    }
    data.update(kwargs)
    return data


def add_endpoint(schema, metadata, path, model, verbose_name, properties, fields, required=(), natural_key=None):
    """Add one creatable list endpoint to the schema and metadata dicts."""
    request_name = f"{model.split('.')[1].title()}Request"
    schema["components"]["schemas"][request_name] = {
        "type": "object",
        "properties": properties,
        "required": list(required),
    }
    schema["paths"][path] = {
        # Like Nautobot, every field can be used as a filter on the list endpoint.
        "get": {"parameters": [{"in": "query", "name": name} for name in ["id", "q", *properties]]},
        "post": {
            "requestBody": {
                "content": {"application/json": {"schema": {"$ref": f"#/components/schemas/{request_name}"}}}
            }
        },
    }
    app_label, model_name = model.split(".")
    metadata["models"][model] = {
        "app_label": app_label,
        "model_name": model_name,
        "verbose_name": verbose_name,
        "verbose_name_plural": f"{verbose_name}s",
        "api_path": f"/api{path}",
        "natural_key": natural_key or ["name"],
        "supports_contacts": False,
        "supports_notes": False,
        "fields": fields,
    }


@pytest.fixture
def api():
    """A schema and metadata with cables, cable types, statuses, tenant groups and dynamic groups."""
    schema = {"openapi": "3.0.3", "paths": {}, "components": {"schemas": {}}}
    metadata = {"nautobot_version": "3.2.8", "models": {}}
    add_endpoint(
        schema,
        metadata,
        "/extras/statuses/",
        "extras.status",
        "status",
        {"name": {"type": "string"}},
        {"name": field_metadata("name", required=True)},
        required=["name"],
    )
    add_endpoint(
        schema,
        metadata,
        "/dcim/cable-types/",
        "dcim.cabletype",
        "cable type",
        {"name": {"type": "string"}, "total_lanes": {"type": "integer"}},
        {"name": field_metadata("name", required=True), "total_lanes": field_metadata("total_lanes")},
        required=["name"],
    )
    add_endpoint(
        schema,
        metadata,
        "/dcim/cables/",
        "dcim.cable",
        "cable",
        {
            "id": {"type": "string", "format": "uuid"},
            "display": {"type": "string", "readOnly": True},
            "label": {"type": "string"},
            "type": {"type": "string"},
            "status": copy.deepcopy(RELATED),
            "tags": {"type": "array", "items": copy.deepcopy(RELATED)},
        },
        {
            "label": field_metadata("label"),
            "type": field_metadata(
                "type", serializer_field="ChoiceField", choices=["cat5", "cat6"], choice_labels=["CAT5", "CAT6"]
            ),
            "status": field_metadata("status", related_model="extras.status", required=True),
        },
        required=["status"],
        natural_key=["pk"],
    )
    add_endpoint(
        schema,
        metadata,
        "/tenancy/tenant-groups/",
        "tenancy.tenantgroup",
        "tenant group",
        {"name": {"type": "string"}},
        {"name": field_metadata("name", required=True)},
        required=["name"],
    )
    add_endpoint(
        schema,
        metadata,
        "/extras/dynamic-groups/",
        "extras.dynamicgroup",
        "dynamic group",
        {"name": {"type": "string"}},
        {"name": field_metadata("name", required=True)},
        required=["name"],
    )
    return schema, metadata


def add_cable_type_field(schema, metadata):
    """Make the schema look like Nautobot 3.2, where cables gained a cable_type for breakout cables."""
    schema["components"]["schemas"]["CableRequest"]["properties"]["cable_type"] = copy.deepcopy(RELATED)
    metadata["models"]["dcim.cable"]["fields"]["cable_type"] = field_metadata(
        "cable_type", related_model="dcim.cabletype", help_text="The cable type defining this cable's lane structure."
    )


@pytest.fixture
def hand_tables():
    """A cut-down copy of the hand-written lookup tables in utils.py."""
    return {
        "API_APPS_ENDPOINTS": {"dcim": ["cables"], "extras": ["statuses"], "tenancy": ["tenant_groups"]},
        "QUERY_TYPES": {"status": "name", "group": "name"},
        "CONVERT_TO_ID": {"status": "statuses", "group": "tenant_groups"},
        "ENDPOINT_NAME_MAPPING": {"cables": "cable"},
        "ALLOWED_QUERY_PARAMS": {"cable": {"label"}, "status": {"name"}},
        "CONVERT_KEYS": {"termination_a": "termination_a_id"},
    }


@pytest.fixture
def cable_config():
    """The config of a hand-written cable module that exposes label, type and status."""
    return {
        "module": "cable",
        "api_path": "/dcim/cables/",
        "endpoint": "cables",
        "header": ["# Copyright: (c) 2020, Test"],
        "utils_module": "dcim",
        "class_name": "NautobotDcimModule",
        "endpoint_constant": "NB_CABLES",
        "instance_var": "cable",
        "main_docstring": "\n    Main entry point for module execution.\n    ",
        "shared_specs": ["NAUTOBOT_ARG_SPEC", "TAGS_ARG_SPEC"],
        "ansible_module_kwargs": {"supports_check_mode": True},
        "extra_imports": [],
        "post_module_code": [],
        "ignore_api_fields": {},
        "lookup_fields": None,
        "generated_examples": False,
        "options": {
            "label": {
                "api_field": "label",
                "argument_spec": {"required": False, "type": "str"},
                "documentation": {"description": ["Label"], "required": False, "type": "str"},
            },
            "type": {
                "api_field": "type",
                "argument_spec": {"required": False, "type": "str", "choices": ["CAT5", "cat5"]},
                "documentation": {
                    "description": ["Type"],
                    "required": False,
                    "type": "str",
                    "choices": ["CAT5", "cat5"],
                },
            },
            "status": {
                "api_field": "status",
                "argument_spec": {"required": False, "type": "raw"},
                "documentation": {"description": ["Status"], "required": False, "type": "raw"},
            },
        },
        "documentation": {
            "module": "cable",
            "short_description": "Create, update or delete cables within Nautobot",
            "description": ["Creates, updates or removes cables from Nautobot"],
            "author": ["Test (@test)"],
            "version_added": "1.0.0",
        },
        "examples": "\n- name: example\n",
        "return": "\ncable:\n  type: dict\n",
    }
