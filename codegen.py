import logging
from pathlib import Path
import json
import re

import jinja2
from prance import ResolvingParser  # TODO: Add prance to poetry. Currently fails with incompatibility with pynautobot


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

    irregulars = {
        "virtual-chassis": "virtual-chassis",
        "object-metadata": "object-metadata",
    }

    if word in irregulars:
        return irregulars[word]

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


def main():
    logger.debug("# Starting code generation for Nautobot modules")

    # Load cached OpenAPI schema from json file if one exists to speed up development
    if Path("openapi-schema.parsed.json").exists():
        with open("openapi-schema.parsed.json") as f:
            spec = json.load(f)
    else:
        # This part takes a long time
        parser = ResolvingParser("openapi-schema.yaml")
        spec = parser.specification
        with open("openapi-schema.parsed.json", "w") as f:
            # Save the parsed OpenAPI schema to a file for future use
            # This will speed up development by avoiding re-parsing the schema each time
            json.dump(spec, f, indent=2)

    logger.debug("# OpenAPI Specification loaded")
    logger.debug("# Generating module code...")

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
        apps[app_label].setdefault(model_name, {"path": path, "methods": {}, "model_name_plural": model_name_plural})

        # TODO: Only testing against dcim.manufacturer for now
        if model_name != "manufacturer":
            continue

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
                            "type": field.get("type", ""),
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
    output_dir = Path("plugins", "modules")

    for app_label, models in apps.items():
        for model_name, model in models.items():
            if model_name != "manufacturer":  # TODO: Only testing against dcim.manufacturer for now
                continue
            template = jinja_env.get_template("plugins/modules/module.py.j2")
            output = template.render(app_label=app_label, model_name=model_name, model=model)
            output_path = output_dir / f"{model_name}.py"
            output_path.write_text(output)
            logger.debug(f"Generated {output_path}")

    logger.debug(json.dumps(apps["dcim"]["manufacturer"], indent=2))


if __name__ == "__main__":
    main()
