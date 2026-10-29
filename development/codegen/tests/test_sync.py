"""Tests for comparing module configs with the API (development/codegen/sync.py)."""

import copy

from development.codegen import schema, sync

from .conftest import add_cable_type_field, field_metadata

SHARED_SPECS = {"NAUTOBOT_ARG_SPEC": {"url", "token", "state"}, "TAGS_ARG_SPEC": {"tags"}, "ID_ARG_SPEC": {"id"}}


def make_context(api, hand_tables, next_version="6.4.0", ignored=()):
    schema_data, metadata = api
    return sync.Context(
        endpoints=schema.parse_endpoints(schema_data, metadata),
        next_version=next_version,
        global_ignored_fields=set(ignored),
        shared_spec_options=SHARED_SPECS,
        hand_tables=hand_tables,
    )


def messages(context, level=None):
    return [message.text for message in context.report.messages if level is None or message.level == level]


def test_breakout_cable_type_is_added_to_the_cable_module(api, hand_tables, cable_config):
    """Nautobot 3.2 added cable_type to cables; the generator adds it to the existing cable module."""
    add_cable_type_field(*api)
    context = make_context(api, hand_tables)

    config = sync.sync_module(cable_config, context.endpoints["/dcim/cables/"], context)

    option = config["options"]["cable_type"]
    assert option["managed"] is True
    assert option["api_field"] == "cable_type"
    assert option["argument_spec"] == {"required": False, "type": "raw"}
    assert option["documentation"]["version_added"] == "6.4.0"
    assert option["documentation"]["description"] == ["The cable type defining this cable's lane structure."]
    assert "added option 'cable_type' for new API field 'cable_type'" in messages(context, sync.INFO)


def test_generated_tables_let_the_new_option_look_up_cable_types_by_name(api, hand_tables, cable_config):
    add_cable_type_field(*api)
    context = make_context(api, hand_tables)
    configs = {"cable": sync.sync_module(cable_config, context.endpoints["/dcim/cables/"], context)}

    tables = sync.build_generated_tables(configs, context)

    assert tables["CONVERT_TO_ID"] == {"cable_type": "cable_types"}
    assert tables["QUERY_TYPES"] == {"cable_type": "name"}
    assert tables["ALLOWED_QUERY_PARAMS"]["cable_type"] == ["name"]
    assert "cable_types" in tables["API_APPS_ENDPOINTS"]["dcim"]
    # Hand-written entries are never repeated in the generated tables.
    assert "cables" not in tables["API_APPS_ENDPOINTS"].get("dcim", [])
    assert "status" not in tables["CONVERT_TO_ID"]


def test_unchanged_api_leaves_the_config_unchanged(api, hand_tables, cable_config):
    cable_config["options"]["type"]["argument_spec"]["choices"] = ["cat5", "cat6"]
    cable_config["options"]["type"]["documentation"]["choices"] = ["cat5", "cat6"]
    context = make_context(api, hand_tables)
    before = copy.deepcopy(cable_config)

    config = sync.sync_module(cable_config, context.endpoints["/dcim/cables/"], context)

    assert config == before
    assert not context.report.messages


def test_removed_api_field_is_an_error(api, hand_tables, cable_config):
    schema_data, metadata = api
    del schema_data["components"]["schemas"]["CableRequest"]["properties"]["label"]
    context = make_context(api, hand_tables)

    sync.sync_module(cable_config, context.endpoints["/dcim/cables/"], context)

    assert any("'label'" in text and "no longer accepts" in text for text in messages(context, sync.ERROR))


def test_new_choice_value_is_added_to_a_hand_written_option(api, hand_tables, cable_config):
    """The hand-written option accepts CAT5/cat5; the API now also has cat6 (label CAT6)."""
    context = make_context(api, hand_tables)

    config = sync.sync_module(cable_config, context.endpoints["/dcim/cables/"], context)

    assert config["options"]["type"]["argument_spec"]["choices"] == ["CAT5", "cat5", "cat6"]
    assert config["options"]["type"]["documentation"]["choices"] == ["CAT5", "cat5", "cat6"]


def test_choice_accepted_by_label_is_not_added(api, hand_tables, cable_config):
    cable_config["options"]["type"]["argument_spec"]["choices"] = ["CAT5", "CAT6"]
    cable_config["options"]["type"]["documentation"]["choices"] = ["CAT5", "CAT6"]
    context = make_context(api, hand_tables)

    config = sync.sync_module(cable_config, context.endpoints["/dcim/cables/"], context)

    assert config["options"]["type"]["argument_spec"]["choices"] == ["CAT5", "CAT6"]


def test_deprecated_module_gets_no_new_options(api, hand_tables, cable_config):
    add_cable_type_field(*api)
    cable_config["documentation"]["deprecated"] = {"removed_in": "7.0.0", "why": "test", "alternative": "test"}
    context = make_context(api, hand_tables)

    config = sync.sync_module(cable_config, context.endpoints["/dcim/cables/"], context)

    assert "cable_type" not in config["options"]


def test_ignored_api_fields_are_not_added(api, hand_tables, cable_config):
    add_cable_type_field(*api)
    cable_config["ignore_api_fields"] = {"cable_type": "test reason"}
    context = make_context(api, hand_tables)

    config = sync.sync_module(cable_config, context.endpoints["/dcim/cables/"], context)

    assert "cable_type" not in config["options"]


def test_managed_option_follows_the_api_but_keeps_its_description(api, hand_tables, cable_config):
    add_cable_type_field(*api)
    context = make_context(api, hand_tables)
    config = sync.sync_module(cable_config, context.endpoints["/dcim/cables/"], context)
    config["options"]["cable_type"]["documentation"]["description"] = ["Written by a person"]
    config["options"]["cable_type"]["known_issue"] = "test"

    # The API turns cable_type into a list of cable types.
    schema_data, metadata = api
    metadata["models"]["dcim.cable"]["fields"]["cable_type"]["many"] = True
    context = make_context(api, hand_tables, next_version="7.0.0")
    config = sync.sync_module(config, context.endpoints["/dcim/cables/"], context)

    option = config["options"]["cable_type"]
    assert option["argument_spec"] == {"required": False, "type": "list", "elements": "raw"}
    assert option["documentation"]["description"] == ["Written by a person"]
    assert option["documentation"]["version_added"] == "6.4.0"
    assert option["known_issue"] == "test"


def test_new_module_options_have_no_version_added(api, hand_tables):
    context = make_context(api, hand_tables)
    endpoint = context.endpoints["/dcim/cable-types/"]
    config = sync.new_module_config("cable_type", endpoint, ("dcim", "NautobotDcimModule"), "6.4.0", set(SHARED_SPECS))

    config = sync.sync_module(config, endpoint, context, is_new=True)

    assert list(config["options"]) == ["name", "total_lanes"]
    assert "version_added" not in config["options"]["name"]["documentation"]
    assert config["documentation"]["version_added"] == "6.4.0"
    assert config["shared_specs"] == ["NAUTOBOT_ARG_SPEC", "ID_ARG_SPEC"]
    assert config["lookup_fields"] == ["name"]


def add_membership_endpoint(api):
    """An endpoint whose `group` field points to dynamic groups, while utils.py maps `group` to tenant groups."""
    schema_data, metadata = api
    from .conftest import RELATED, add_endpoint  # pylint: disable=import-outside-toplevel

    add_endpoint(
        schema_data,
        metadata,
        "/extras/dynamic-group-memberships/",
        "extras.dynamicgroupmembership",
        "dynamic group membership",
        {"group": copy.deepcopy(RELATED), "weight": {"type": "integer"}},
        {
            "group": field_metadata("group", related_model="extras.dynamicgroup", required=True),
            "weight": field_metadata("weight"),
        },
        required=["group"],
        natural_key=["group__name", "weight"],
    )


def test_option_clashing_with_convert_to_id_is_renamed(api, hand_tables):
    add_membership_endpoint(api)
    context = make_context(api, hand_tables)
    endpoint = context.endpoints["/extras/dynamic-group-memberships/"]
    config = sync.new_module_config(
        "dynamic_group_membership", endpoint, ("extras", "NautobotExtrasModule"), "6.4.0", set(SHARED_SPECS)
    )

    config = sync.sync_module(config, endpoint, context, is_new=True)
    tables = sync.build_generated_tables({"dynamic_group_membership": config}, context)

    assert "group" not in config["options"]
    assert config["options"]["dynamic_group"]["api_field"] == "group"
    assert tables["ENDPOINT_CONVERT_KEYS"] == {"dynamic_group_memberships": {"dynamic_group": "group"}}
    assert tables["CONVERT_TO_ID"]["dynamic_group"] == "dynamic_groups"
    # The module's own lookup uses the option names.
    assert tables["ALLOWED_QUERY_PARAMS"]["dynamic_group_membership"] == ["dynamic_group", "weight"]


def test_option_name_that_cannot_be_renamed_is_an_error(api, hand_tables):
    """A plain string field named like a CONVERT_TO_ID key has no object type to be renamed after."""
    schema_data, metadata = api
    schema_data["components"]["schemas"]["CabletypeRequest"]["properties"]["group"] = {"type": "string"}
    metadata["models"]["dcim.cabletype"]["fields"]["group"] = field_metadata("group")
    context = make_context(api, hand_tables)
    endpoint = context.endpoints["/dcim/cable-types/"]
    config = sync.new_module_config("cable_type", endpoint, ("dcim", "NautobotDcimModule"), "6.4.0", set(SHARED_SPECS))

    config = sync.sync_module(config, endpoint, context, is_new=True)

    assert "group" not in config["options"]
    assert any("API field 'group' needs an option name" in text for text in messages(context, sync.ERROR))


def test_foreign_key_looked_up_on_the_wrong_endpoint_is_an_error(api, hand_tables, cable_config):
    hand_tables["CONVERT_TO_ID"]["status"] = "tenant_groups"
    context = make_context(api, hand_tables)
    configs = {"cable": sync.sync_module(cable_config, context.endpoints["/dcim/cables/"], context)}

    sync.check_foreign_keys(configs, sync.build_generated_tables(configs, context), context)

    assert any("'status' is looked up on 'tenancy.tenant_groups'" in text for text in messages(context, sync.ERROR))


def test_known_issue_turns_the_foreign_key_error_into_a_warning(api, hand_tables, cable_config):
    hand_tables["CONVERT_TO_ID"]["status"] = "tenant_groups"
    cable_config["options"]["status"]["known_issue"] = "tracked elsewhere"
    context = make_context(api, hand_tables)
    configs = {"cable": sync.sync_module(cable_config, context.endpoints["/dcim/cables/"], context)}

    sync.check_foreign_keys(configs, sync.build_generated_tables(configs, context), context)

    assert not context.report.errors
    assert any("known issue: tracked elsewhere" in text for text in messages(context, sync.WARNING))


def test_foreign_key_in_another_app_with_the_same_endpoint_name_is_an_error(api, hand_tables, cable_config):
    """`interfaces` exists in dcim and virtualization; utils.py always resolves the first app that lists it."""
    hand_tables["API_APPS_ENDPOINTS"]["tenancy"].append("statuses")
    hand_tables["API_APPS_ENDPOINTS"] = {
        "tenancy": hand_tables["API_APPS_ENDPOINTS"]["tenancy"],
        **{key: value for key, value in hand_tables["API_APPS_ENDPOINTS"].items() if key != "tenancy"},
    }
    context = make_context(api, hand_tables)
    configs = {"cable": sync.sync_module(cable_config, context.endpoints["/dcim/cables/"], context)}

    sync.check_foreign_keys(configs, sync.build_generated_tables(configs, context), context)

    assert any("'tenancy.statuses'" in text for text in messages(context, sync.ERROR))


def test_hand_written_option_names_are_not_added_to_convert_to_id(api, hand_tables, cable_config):
    """Adding a CONVERT_TO_ID entry for a hand-written option would change how that module resolves values."""
    add_cable_type_field(*api)
    cable_config["options"]["cable_type"] = {
        "api_field": "cable_type",
        "argument_spec": {"required": False, "type": "raw"},
        "documentation": {"description": ["x"], "required": False, "type": "raw"},
    }
    context = make_context(api, hand_tables)
    configs = {"cable": sync.sync_module(cable_config, context.endpoints["/dcim/cables/"], context)}

    tables = sync.build_generated_tables(configs, context)

    assert "cable_type" not in tables["CONVERT_TO_ID"]


def test_argument_spec_types():
    def spec(**kwargs):
        return sync.argument_spec_for_field(schema.ApiField(name=kwargs.pop("name", "x"), **kwargs))

    assert spec(json_type="boolean", required=False) == {"required": False, "type": "bool"}
    assert spec(json_type="number", required=False) == {"required": False, "type": "float"}
    assert spec(json_type="array", json_items_type="string", required=False) == {
        "required": False,
        "type": "list",
        "elements": "str",
    }
    assert spec(json_type="string", required=False, related_model="contenttypes.contenttype", content_type=True) == {
        "required": False,
        "type": "str",
    }
    assert spec(
        json_type="array", required=False, related_model="contenttypes.contenttype", content_type=True, many=True
    ) == {"required": False, "type": "list", "elements": "str"}
    assert spec(name="password", json_type="string", required=False) == {
        "required": False,
        "type": "str",
        "no_log": True,
    }
    assert spec(name="secrets_group", json_type="object", required=False, related_model="extras.secretsgroup") == {
        "required": False,
        "type": "raw",
        "no_log": False,
    }


def test_next_minor_version():
    assert sync.next_minor_version("6.3.0") == "6.4.0"
    assert sync.next_minor_version("6.10.2") == "6.11.0"


def test_module_name_for_endpoint(api, hand_tables):
    context = make_context(api, hand_tables)
    assert sync.module_name_for_endpoint(context.endpoints["/dcim/cable-types/"]) == "cable_type"


def test_natural_key_with_a_field_the_api_cannot_filter_on_falls_back_to_name(api, hand_tables):
    schema_data, metadata = api
    metadata["models"]["dcim.cabletype"]["natural_key"] = ["manufacturer__name", "part_number"]
    context = make_context(api, hand_tables)

    assert sync.natural_key_fields(context.endpoints["/dcim/cable-types/"]) == ["name"]


def test_model_without_a_usable_natural_key_is_found_by_id_only(api, hand_tables):
    """Cables have a `pk` natural key and no name: guessing fields could update the wrong cable."""
    context = make_context(api, hand_tables)

    assert sync.natural_key_fields(context.endpoints["/dcim/cables/"]) == []


def test_lookup_fields_must_be_list_filters(api, hand_tables):
    schema_data, _ = api
    parameters = schema_data["paths"]["/dcim/cable-types/"]["get"]["parameters"]
    schema_data["paths"]["/dcim/cable-types/"]["get"]["parameters"] = [p for p in parameters if p["name"] != "name"]
    context = make_context(api, hand_tables)

    assert sync.natural_key_fields(context.endpoints["/dcim/cable-types/"]) == []
    assert sync.primary_lookup(context.endpoints["/dcim/cable-types/"]) is None


def test_foreign_key_lookup_entry_never_reuses_a_module_lookup_key(api, hand_tables, cable_config):
    """ALLOWED_QUERY_PARAMS["cable_type"] would also be the cable_type module's own lookup."""
    add_cable_type_field(*api)
    context = make_context(api, hand_tables)
    configs = {"cable": sync.sync_module(cable_config, context.endpoints["/dcim/cables/"], context)}
    endpoint = context.endpoints["/dcim/cable-types/"]
    new_config = sync.new_module_config(
        "cable_type", endpoint, ("dcim", "NautobotDcimModule"), "6.4.0", set(SHARED_SPECS)
    )
    new_config["lookup_fields"] = ["name", "total_lanes"]
    configs["cable_type"] = sync.sync_module(new_config, endpoint, context, is_new=True)

    tables = sync.build_generated_tables(configs, context)

    assert tables["ALLOWED_QUERY_PARAMS"]["cable_type"] == ["name", "total_lanes"]
    assert tables["CONVERT_TO_ID"]["cable_type"] == "cable_types"


def test_module_without_lookup_fields_gets_an_empty_lookup_and_a_warning(api, hand_tables):
    context = make_context(api, hand_tables)
    endpoint = context.endpoints["/dcim/cable-types/"]
    config = sync.new_module_config("cable_type", endpoint, ("dcim", "NautobotDcimModule"), "6.4.0", set(SHARED_SPECS))
    config["lookup_fields"] = []
    config = sync.sync_module(config, endpoint, context, is_new=True)

    tables = sync.build_generated_tables({"cable_type": config}, context)

    assert tables["ALLOWED_QUERY_PARAMS"]["cable_type"] == []
    assert any("finds existing objects by `id` only" in text for text in messages(context, sync.WARNING))


def test_write_only_fields_of_generated_options_are_listed_per_endpoint(api, hand_tables, cable_config):
    add_cable_type_field(*api)
    _, metadata = api
    metadata["models"]["dcim.cable"]["fields"]["cable_type"]["write_only"] = True
    cable_config["options"]["label"]["api_field"] = "label"
    context = make_context(api, hand_tables)
    configs = {"cable": sync.sync_module(cable_config, context.endpoints["/dcim/cables/"], context)}

    tables = sync.build_generated_tables(configs, context)

    # Only generator-managed options are listed; hand-written modules handle write-only fields themselves.
    assert tables["ENDPOINT_WRITE_ONLY_FIELDS"] == {"cables": ["cable_type"]}
