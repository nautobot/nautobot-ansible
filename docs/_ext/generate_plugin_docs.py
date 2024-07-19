"""This generates the plugin documentation for Mkdocs-Material."""

import json
import logging
import os

from jinja2 import Environment, FileSystemLoader

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    template = env.get_template("modules.md.j2")

    # Generate the plugin documentation, getting to the plugins which are in the ['all']['module'] key
    for plugin_name, plugin_values in plugins['all']['module'].items():
        # Create the plugin directory
        plugin_dir = os.path.join("docs", "plugins")
        os.makedirs(plugin_dir, exist_ok=True)

        # Grab specific variables to make the Jinja templating easier
        # breakpoint()
        authors = plugin_values['doc']['author']
        collection_name = plugin_values['doc']['collection']
        description = plugin_values['doc']['description']
        notes = plugin_values['doc'].get('notes')
        parameters = plugin_values['doc']['options']
        version_added = plugin_values['doc']['version_added']
        examples = plugin_values['examples']
        return_data = plugin_values['return']
        requirements = plugin_values['doc']['requirements']

        # Generate the plugin documentation
        plugin_doc = template.render(
            plugin_name=plugin_name,
            authors=authors,
            collection_name=collection_name,
            description=description,
            notes=notes,
            parameters=parameters,
            version_added=version_added,
            examples=examples,
            return_data=return_data,
            requirements=requirements,
            plugin_values=plugin_values,
        )
        
        # Get the module name from the ansible-docs output for the file name.
        module_name = plugin_values['doc']['module']
        with open(os.path.join(plugin_dir, module_name + ".md"), "w") as f:
            f.write(plugin_doc)
            logger.info(f"Generated documentation for {module_name}")


# TODOs
# Check into the conversion of C() and E()
