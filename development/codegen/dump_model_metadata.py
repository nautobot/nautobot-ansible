"""Dump REST API model metadata from a running Nautobot instance as JSON.

The OpenAPI schema doesn't say which model a foreign key points to, which fields make up a model's natural key,
or what most fields mean. This script reads that from Nautobot's models and REST API serializers.

Run it inside the Nautobot container:

    nautobot-server shell < dump_model_metadata.py > model_metadata.json

The output is consumed by `development/codegen/generate.py`.
"""

import json
import sys

import nautobot
from django.apps import apps
from django.urls import NoReverseMatch, resolve, reverse
from nautobot.core.api.fields import ChoiceField, ContentTypeField
from nautobot.core.utils.lookup import get_route_for_model
from rest_framework import serializers
from rest_framework.relations import ManyRelatedField, RelatedField

BEGIN_MARKER = "----- BEGIN MODEL METADATA -----"
END_MARKER = "----- END MODEL METADATA -----"


def _label(model):
    return f"{model._meta.app_label}.{model._meta.model_name}"


def _related_model(field):
    """Return the model a serializer related field points to, or None."""
    queryset = getattr(field, "queryset", None)
    if queryset is not None:
        return queryset.model
    return None


def _field_metadata(name, field):
    """Return the metadata for one serializer field."""
    data = {
        "name": name,
        "serializer_field": type(field).__name__,
        "read_only": bool(field.read_only),
        "write_only": bool(field.write_only),
        "required": bool(field.required),
        "allow_null": bool(getattr(field, "allow_null", False)),
        "help_text": str(field.help_text) if field.help_text else None,
        "label": str(field.label) if field.label else None,
        "many": False,
        "related_model": None,
        "choices": None,
        "choice_labels": None,
        "content_types": None,
    }
    if isinstance(field, ManyRelatedField):
        data["many"] = True
        field = field.child_relation
    elif isinstance(field, serializers.ListSerializer):
        data["many"] = True
        field = field.child

    if isinstance(field, ContentTypeField):
        data["related_model"] = "contenttypes.contenttype"
        queryset = getattr(field, "queryset", None)
        if queryset is not None:
            try:
                data["content_types"] = sorted(f"{ct.app_label}.{ct.model}" for ct in queryset)
            except Exception:  # noqa: BLE001 - queryset may need a database that isn't populated
                data["content_types"] = None
    elif isinstance(field, RelatedField):
        related = _related_model(field)
        if related is not None:
            data["related_model"] = _label(related)
    elif isinstance(field, (ChoiceField, serializers.ChoiceField)):
        choices = field.choiceset if isinstance(field, ChoiceField) else field.choices.items()
        values = []
        labels = []
        for key, value in choices:
            # Choices can be grouped: (group label, ((value, label), ...)).
            if isinstance(value, (list, tuple)):
                values.extend(str(k) for k, _ in value)
                labels.extend(str(v) for _, v in value)
            else:
                values.append(str(key))
                labels.append(str(value))
        data["choices"] = values
        data["choice_labels"] = labels
    return data


def _natural_key(model):
    try:
        return list(model.natural_key_field_lookups)
    except Exception:  # noqa: BLE001 - not every model can compute a natural key
        return None


def dump():
    """Return a dict of metadata for every model that has a REST API list endpoint."""
    output = {"nautobot_version": nautobot.__version__, "models": {}}
    for model in apps.get_models():
        try:
            path = reverse(get_route_for_model(model, "list", api=True))
        except (NoReverseMatch, LookupError):
            continue
        view = resolve(path).func
        viewset = getattr(view, "cls", None)
        serializer_class = getattr(viewset, "serializer_class", None)
        if serializer_class is None:
            continue
        try:
            serializer = serializer_class(context={"request": None})
            fields = serializer.fields
        except Exception as exc:  # noqa: BLE001
            print(f"Unable to load serializer for {_label(model)}: {exc}", file=sys.stderr)
            continue

        model_fields = {}
        for model_field in model._meta.get_fields():
            help_text = getattr(model_field, "help_text", "")
            if help_text:
                model_fields[model_field.name] = str(help_text)

        output["models"][_label(model)] = {
            "app_label": model._meta.app_label,
            "model_name": model._meta.model_name,
            "verbose_name": str(model._meta.verbose_name),
            "verbose_name_plural": str(model._meta.verbose_name_plural),
            "api_path": path,
            "natural_key": _natural_key(model),
            "supports_contacts": bool(getattr(model, "is_contact_associable_model", False)),
            "supports_notes": "notes_url" in fields,
            "fields": {
                name: {**_field_metadata(name, field), "model_help_text": model_fields.get(name)}
                for name, field in fields.items()
            },
        }
    return output


# `nautobot-server shell` can print its own messages to stdout, so the JSON goes between markers
# that `generate.py` looks for.
print(BEGIN_MARKER)
json.dump(dump(), sys.stdout, indent=2, sort_keys=True)
print()
print(END_MARKER)
