import datetime
import json
import logging
import re
import subprocess
import sys
from pathlib import Path

import jinja2
import requests
from prance import ResolvingParser

logger = logging.getLogger(__name__)

OUT_OF_SCOPE_PATHS = [
    "/graphql/",
    "/swagger/",
    "/swagger.json",
    "/swagger.yaml",
    "/ui/core/",
    "/metrics/",
    "/core/render-jinja-template/",
    "/ui/core/render-jinja-template/",
    "/status/",
    r"/ipam/vlan-groups/{id}/available-vlans/",  # TODO: Handle special endpoints like this one
]


def singularize(word):
    word = word.lower()

    non_standard = {
        "virtual-chassis": "virtual-chassis",
        "object-metadata": "object-metadata",
    }

    if word in non_standard:
        return non_standard[word]

    # Rules for regular plural forms
    if word.endswith("ies"):
        return re.sub(r"ies$", "y", word)
    elif word.endswith("ves"):
        return re.sub(r"ves$", "f", word)
    elif word.endswith("ses") or word.endswith("xes"):
        return word[:-2]
    elif word.endswith("s") and not word.endswith("ss"):
        return word[:-1]

    return word


def openapi_type_to_ansible_type(openapi_type):
    mapping = {
        "": "str",  # default value is str
        "array": "list",
        "boolean": "bool",
        "integer": "int",
        "number": "int",
        "object": "dict",
        "string": "str",
    }
    if openapi_type not in mapping:
        raise ValueError(f"No ansible type found for openapi type '{openapi_type}'")

    return mapping[openapi_type]


def field_example_value(field):
    if field["name"] == "status" and field["type"] == "string":
        return '"Active"'
    if field["type"] == "string":
        if field["choices"] is not None:
            return field["choices"][0]
        return f'"Test {field["name"].replace("_", " ").title()}"'


def _get_field_type(field_name, field_properties):
    field_type = ""
    if "type" in field_properties:
        field_type = field_properties["type"]
    elif "oneOf" in field_properties:
        for candidate in field_properties["oneOf"]:
            if "type" not in candidate:
                continue
            field_type = candidate.get("type")

    # Special handling for status
    if field_name == "status" and field_type == "object":
        return "string"

    return field_type


def _get_field_choices(field_properties):
    choices = field_properties.get("enum", None) or None
    if "oneOf" in field_properties:
        for candidate in field_properties["oneOf"]:
            if "enum" in candidate and any(choice for choice in candidate["enum"]):
                choices = candidate["enum"]
    if choices is not None:
        return sorted(choices)
    return choices


def main():
    logging_level = logging.DEBUG if "--debug" in sys.argv else logging.INFO
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging_level, stream=sys.stdout)
    logger.info("Starting code generation for Nautobot modules")

    # Load cached OpenAPI schema from json file if one exists to speed up development
    cached_schema_file = "openapi-schema.parsed.json"
    if Path(cached_schema_file).exists():
        logger.info(f"Reusing cached schema from file '{cached_schema_file}'.")
        with open(cached_schema_file) as f:
            spec = json.load(f)
    else:
        schema_url = "https://demo.nautobot.com/api/swagger/"
        schema_api_key = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        schema_file = "openapi-schema.json"
        logger.info(f"Retrieving schema from '{schema_url}'.")
        schema_response = requests.get(
            schema_url, timeout=30, headers={"Authorization": f"Token {schema_api_key}", "Accept": "application/json"}
        )
        if schema_response.ok:
            logger.info(f"Saving schema to '{schema_file}'.")
            with open(schema_file, "w") as f:
                f.write(schema_response.text)
        logger.info("Parsing OpenAPI schema. This may take a while...")
        parser = ResolvingParser(schema_file)
        spec = parser.specification
        with open(cached_schema_file, "w") as f:
            # Save the parsed OpenAPI schema to a file for future use
            # This will speed up development by avoiding re-parsing the schema each time
            json.dump(spec, f, indent=2)

    logger.debug("OpenAPI Specification loaded")
    logger.debug("Generating module code...")

    apps = {}

    for path, path_item in spec.get("paths", {}).items():
        if path in OUT_OF_SCOPE_PATHS:
            logger.debug(f"Skipping path: {path} (out of scope)")
            continue

        try:
            app_label, model_name_plural = path.split("/")[1:3]
        except ValueError:
            logger.debug(f"Skipping path: {path} (not in expected format)")
            continue
        if app_label == "plugins":
            logger.debug(f"Skipping path: {path} (example-app)")
            continue
        if len(path.split("/")) != 4:
            logger.debug(f"Skipping path: {path} (not in expected format)")
            continue
        app_label = app_label.replace("-", "_")
        model_name = singularize(model_name_plural).replace("-", "_")
        apps.setdefault(app_label, {})
        apps[app_label].setdefault(
            model_name, {"path": path, "methods": {}, "model_name_plural": model_name_plural, "fields": {}}
        )

        for method, operation in path_item.items():
            if method.lower() not in ["get", "post"]:  # TODO: support ["put", "delete", "patch", "options", "head"]
                continue

            method_dict = {}
            method_dict["operationId"] = operation.get("operationId", "")
            method_dict["summary"] = operation.get("summary", "")
            # operation.keys = ['operationId', 'description', 'parameters', 'tags', 'requestBody', 'security', 'responses']
            # GET operation["responses"]["200"].keys = ['content', 'description']
            # GET operation["responses"]["200"]["content"]["application/json"]["schema"].keys = ['type', 'required', 'properties']

            # All the interesting stuff for a GET request is in
            # operation["responses"]["200"]["content"]["application/json"]["schema"]["properties"]["results"]["items"]["properties"]
            # operation["responses"]["200"]["content"]["application/json"]["schema"]["properties"]["results"]["items"]["required"]
            if method.lower() == "get":
                try:
                    responses = operation["responses"]["200"]["content"]["application/json"]["schema"]["properties"][
                        "results"
                    ]["items"]
                except KeyError:
                    # TODO: Only list views return a "results" key
                    logger.debug(f"Skipping path: {path} (no results in GET response)")
                    continue
                try:
                    method_dict["properties"] = responses["properties"]
                    method_dict["required"] = responses["required"]
                except KeyError:
                    logger.debug(f"Skipping path: {path} (no properties in GET response)")
                    continue

            # All the interesting stuff for a POST request is in
            # operation["requestBody"]["content"]["application/json"]["schema"]["properties"]
            # operation["requestBody"]["content"]["application/json"]["schema"]["required"]
            else:
                try:
                    request_body = operation["requestBody"]["content"]["application/json"]["schema"]
                except KeyError:
                    logger.debug(f"Skipping path: {path} (no request body in {method.upper()} request)")
                    continue
                try:
                    method_dict["properties"] = request_body.get("properties", {})
                    method_dict["required"] = request_body.get("required", [])
                    fields = {}
                    for field_name, field in method_dict["properties"].items():
                        fields[field_name] = {
                            "name": field_name,
                            "type": _get_field_type(field_name, field),
                            "choices": _get_field_choices(field),
                            "required": field_name in method_dict["required"],
                        }
                    apps[app_label][model_name]["fields"] = fields

                except KeyError:
                    logger.debug(f"Skipping path: {path} (no properties in {method.upper()} request)")
                    continue

            apps[app_label][model_name]["methods"][method.lower()] = method_dict

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("codegen_templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    jinja_env.filters["openapi_type_to_ansible_type"] = openapi_type_to_ansible_type
    jinja_env.filters["field_example_value"] = field_example_value

    output_dir = Path("plugins", "modules")

    for app_label, models in apps.items():
        for model_name, model in models.items():
            # if model_name != "cable":  # TODO: Only testing against dcim.cable for now
            #     continue
            template = jinja_env.get_template("plugins/modules/model_name.py.j2")
            try:
                output = template.render(
                    app_label=app_label, model_name=model_name, model=model, date=datetime.date.today()
                )
            except jinja2.exceptions.TemplateError:
                logger.exception(f"Failed to render template for {model_name}. Skipping")
                continue
            output_path = output_dir / f"{model_name}.py"
            output_path.write_text(output)
            logger.debug(f"Generated {output_path}")

    logger.debug(json.dumps(apps["dcim"]["cable"]["methods"]["post"], indent=2))

    logger.info("Formatting files with ruff")
    subprocess.run(["ruff", "check", "--select", "I", "--fix", (Path(__file__).parent / "plugins").absolute()])  # noqa: S603,S607
    subprocess.run(["ruff", "format", (Path(__file__).parent / "plugins").absolute()])  # noqa: S603,S607

    logger.info("Code generation complete")


if __name__ == "__main__":
    main()
