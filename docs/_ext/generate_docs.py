"""This generates the plugin documentation for Mkdocs-Material."""

import json
import logging
import os

from jinja2 import Environment, FileSystemLoader

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def parse_json_info(plugin_values):
    """Parses the dictionary information into individual fragments.

    Args:
        plugin_values (dict): JSON dictionary of the plugin values

    Returns:
        dict: Dictionary of the parsed values
    """

    return_dict = {}

    return_dict["authors"] = plugin_values['doc'].get("author")
    return_dict["collection_name"] = plugin_values['doc'].get("collection")
    return_dict["description"] = plugin_values['doc'].get("description")
    return_dict["notes"] = plugin_values['doc'].get('notes')
    return_dict["parameters"] = plugin_values['doc'].get("options")
    return_dict["version_added"] = plugin_values['doc'].get("version_added")
    return_dict["examples"] = plugin_values['examples']
    return_dict["return_data"] = plugin_values['return']
    return_dict["requirements"] = plugin_values['doc'].get("requirements")

    return return_dict

def generate_module_markdown(plugin_name, plugin_values):
    """Generates the module docs.

    Args:
        plugin_name (str): The name of the plugin
        plugin_values (dict): JSON dictionary of the plugin values
    """
    # Grab specific variables to make the Jinja templating easier
    # breakpoint()
    template_vars = parse_json_info(plugin_values)

    # logger.info(f"Generating documentation for {plugin_name}")
    # if plugin_name == "networktocode.nautobot.inventory":
    #     breakpoint()

    # Generate the plugin documentation
    plugin_doc = template.render(
        plugin_name=plugin_name,
        plugin_values=plugin_values,
        **template_vars
    )

    return plugin_doc

def loop_over_component(plugin_data, component, doc_type):
    """Iterate over the various plugin types.

    Args:
        plugin_data (dict): Data from the ansible-doc output
        component (str): Component to iterate over, such as "module" or "inventory"
        doc_type (str): Type of documentation to generate, such as "plugin" or "inventory", corresponds to the output directory
    """
    for plugin_name, plugin_values in plugins['all'][component].items():
        # Create the plugin directory
        plugin_dir = os.path.join("docs", doc_type)
        os.makedirs(plugin_dir, exist_ok=True)

        plugin_doc = generate_module_markdown(plugin_name, plugin_values)
        
        # Get the module name from the ansible-docs output for the file name.
        match component:
            case "module":
                name_key = "module"
            case "inventory":
                name_key = "name"
            case "lookup":
                name_key = "name"
            case _:
                raise ValueError(f"Unknown component {component}")
        module_name = plugin_values['doc'][name_key]
        with open(os.path.join(plugin_dir, module_name + ".md"), "w") as f:
            f.write(plugin_doc)
            logger.info(f"Generated documentation for {module_name}")

if __name__ == "__main__":
    # Load the plugin data
    with open("docs/_ext/docs_spec.json", "r") as f:
        plugins = json.load(f)

    # Load the template
    env = Environment(
        loader=FileSystemLoader("docs/_templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    

    # Generate the plugin documentation, getting to the plugins which are in the ['all']['module'] key
    for component, doc_type in [
        ("module", "plugins"),
        ("inventory", "inventory"),
        ("lookup", "lookup"),
        # ("filter", "filter"),
    ]:
        template = env.get_template(f"{component}.md.j2")
        loop_over_component(plugins, component, doc_type)


# TODOs
# Check into the conversion of C() and E()
# Inventory:
#  - Check for keyed_groups if we should do anything with that
#  - Handle various types of plugins that are not part of the Nautobot collection
