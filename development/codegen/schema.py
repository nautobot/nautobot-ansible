"""Read the Nautobot OpenAPI schema and model metadata into per-endpoint field descriptions."""

import re
from dataclasses import dataclass, field

# Fields every module gets from shared argument specs or that the API manages itself.
COMMON_FIELDS = {
    "computed_fields",
    "created",
    "custom_fields",
    "display",
    "id",
    "last_updated",
    "natural_slug",
    "notes_url",
    "object_type",
    "relationships",
    "tags",
    "url",
}

BEGIN_MARKER = "----- BEGIN MODEL METADATA -----"
END_MARKER = "----- END MODEL METADATA -----"


@dataclass
class ApiField:
    """One writable field on a Nautobot REST API endpoint."""

    name: str
    json_type: str
    required: bool
    nullable: bool = False
    many: bool = False
    related_model: str = None
    choices: list = None
    choice_labels: list = None
    help_text: str = None
    json_items_type: str = None
    content_type: bool = False
    write_only: bool = False


@dataclass
class Endpoint:
    """A Nautobot REST API list endpoint that supports POST."""

    path: str
    app: str
    endpoint: str
    model: str
    verbose_name: str
    natural_key: list
    supports_contacts: bool
    supports_notes: bool
    fields: dict = field(default_factory=dict)
    creatable: bool = True
    filter_params: set = field(default_factory=set)
    tags_supported: bool = False
    custom_fields_supported: bool = False


def extract_metadata_json(output):
    """Return the JSON text that `dump_model_metadata.py` printed between its markers."""
    start = output.find(BEGIN_MARKER)
    end = output.find(END_MARKER)
    if start == -1 or end == -1 or end < start:
        raise ValueError("Model metadata markers not found in the output of dump_model_metadata.py")
    return output[start + len(BEGIN_MARKER) : end].strip()


def api_name_to_attr(name):
    """Convert a URL path segment to the attribute name pynautobot uses (`ip-addresses` -> `ip_addresses`)."""
    return name.replace("-", "_")


def _resolve_ref(schema, node):
    while isinstance(node, dict) and "$ref" in node:
        name = node["$ref"].split("/")[-1]
        node = schema["components"]["schemas"][name]
    return node


def _json_type(schema, node):
    """Return (type, items_type) for an OpenAPI property, looking through `$ref`, `allOf` and `oneOf`."""
    node = _resolve_ref(schema, node)
    if "type" in node:
        items_type = None
        if node["type"] == "array":
            items_type, _ = _json_type(schema, node.get("items", {}))
        return node["type"], items_type
    for key in ("allOf", "oneOf", "anyOf"):
        for candidate in node.get(key, []):
            candidate_type, items_type = _json_type(schema, candidate)
            if candidate_type:
                return candidate_type, items_type
    return "", None


def _request_schema(schema, path_item):
    try:
        content = path_item["post"]["requestBody"]["content"]["application/json"]["schema"]
    except KeyError:
        return None
    content = _resolve_ref(schema, content)
    # Bulk-capable endpoints describe the request body as "one object or a list of objects".
    for key in ("oneOf", "anyOf"):
        for candidate in content.get(key, []):
            candidate = _resolve_ref(schema, candidate)
            if candidate.get("type") == "object":
                return candidate
    return content


def parse_endpoints(schema, metadata):
    """Build an Endpoint for every creatable list endpoint found in both the schema and the metadata.

    Args:
        schema (dict): The OpenAPI schema from `nautobot-server spectacular`.
        metadata (dict): The output of `dump_model_metadata.py`.

    Returns:
        (dict): Endpoint objects keyed by API path (for example `/ipam/vlans/`).
    """
    models_by_path = {}
    for label, model in metadata["models"].items():
        api_path = re.sub(r"^/api", "", model["api_path"])
        models_by_path[api_path] = (label, model)

    endpoints = {}
    for path, path_item in schema["paths"].items():
        if not re.fullmatch(r"/[^/{}]+/[^/{}]+/", path) or path not in models_by_path:
            continue
        # Endpoints without POST (such as /extras/jobs/) get no module, but options can still point to them.
        request_schema = _request_schema(schema, path_item) if "post" in path_item else None
        label, model = models_by_path[path]
        app, endpoint_name = path.strip("/").split("/")
        required = set((request_schema or {}).get("required", []))
        properties = (request_schema or {}).get("properties", {})

        endpoint = Endpoint(
            path=path,
            app=api_name_to_attr(app),
            endpoint=api_name_to_attr(endpoint_name),
            model=label,
            verbose_name=model["verbose_name"],
            natural_key=model["natural_key"] or [],
            supports_contacts=model.get("supports_contacts", False),
            supports_notes=model.get("supports_notes", False),
            creatable=request_schema is not None,
            filter_params={parameter.get("name") for parameter in path_item.get("get", {}).get("parameters", [])},
            tags_supported="tags" in properties,
            custom_fields_supported="custom_fields" in properties,
        )
        for name, prop in properties.items():
            if name in COMMON_FIELDS:
                continue
            resolved = _resolve_ref(schema, prop)
            if resolved.get("readOnly"):
                continue
            field_metadata = model["fields"].get(name, {})
            if field_metadata.get("read_only"):
                continue
            json_type, items_type = _json_type(schema, prop)
            help_text = field_metadata.get("help_text") or field_metadata.get("model_help_text")
            endpoint.fields[name] = ApiField(
                name=name,
                json_type=json_type,
                json_items_type=items_type,
                required=name in required,
                nullable=bool(resolved.get("nullable")),
                many=bool(field_metadata.get("many")),
                related_model=field_metadata.get("related_model"),
                choices=field_metadata.get("choices"),
                choice_labels=field_metadata.get("choice_labels"),
                help_text=help_text,
                content_type=field_metadata.get("related_model") == "contenttypes.contenttype",
                write_only=bool(field_metadata.get("write_only")),
            )
        endpoints[path] = endpoint
    return endpoints


def model_endpoints(endpoints):
    """Map each model label (`ipam.vlan`) to the Endpoint that manages it."""
    return {endpoint.model: endpoint for endpoint in endpoints.values()}
