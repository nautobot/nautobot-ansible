import os
import re
import yaml
import sys
from collections import defaultdict

# Add the plugins directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../plugins')))

from doc_fragments.fragments import ModuleDocFragment

env_var_usage = defaultdict(list)

def extract_section(content, section_name):
    pattern = re.compile(rf'{section_name} = r?""".*?"""', re.DOTALL)
    match = pattern.search(content)
    if match:
        return match.group(0).strip().strip(f'{section_name} = r"""').strip(f'{section_name} = """').strip()
    return ""

def extract_fragments(content):
    fragments = []
    pattern = re.compile(r'extends_documentation_fragment:\n  - (.+)')
    match = pattern.search(content)
    if match:
        fragments = match.group(1).split('\n  - ')
    return fragments

def merge_fragments(main_doc, fragments):
    main_doc_yaml = yaml.safe_load(main_doc)
    for fragment in fragments:
        fragment_content = getattr(ModuleDocFragment, fragment.split('.')[-1].upper(), "")
        if fragment_content:
            fragment_yaml = yaml.safe_load(fragment_content)
            if 'options' in fragment_yaml:
                if 'options' not in main_doc_yaml:
                    main_doc_yaml['options'] = {}
                main_doc_yaml['options'].update(fragment_yaml['options'])
    return yaml.dump(main_doc_yaml)

def extract_synopsis(documentation):
    synopsis_pattern = re.compile(r'description:\n(  - .+?\n)+', re.DOTALL)
    match = synopsis_pattern.search(documentation)
    if match:
        synopsis = match.group(0).split("\n")[1].strip().strip("- ").strip()
        return synopsis
    return "No synopsis available."

def format_description(description_lines, module_name):
    """
    Format the description lines to handle multiple bullet points.
    """
    formatted_description = ""
    for line in description_lines:
        # Replace C(code) with `code`
        line = re.sub(r'C\((.+?)\)', r'`\1`', line)
        # Replace E(env_var) with a link to the environment variables reference
        env_vars = re.findall(r'E\((.+?)\)', line)
        for env_var in env_vars:
            env_var_usage[env_var].append(module_name)
            line = line.replace(f'E({env_var})', f'[`{env_var}`](../code_reference/environment_variables.md#{env_var.lower()})')
        if line.startswith("- "):
            formatted_description += f"<li>{line.strip('- ').strip()}</li>\n"
        else:
            formatted_description += f"{line.strip()}\n"
    return formatted_description

def format_multiline(text):
    """
    Format multiline text for Markdown tables, ensuring proper line breaks and handling special cases.
    """
    text = text.replace('\n', ' ').replace('  ', ' ').strip()
    return text

def convert_to_markdown(file_name, documentation, examples, return_section, fragments):
    module_name = f"networktocode.nautobot.{os.path.splitext(file_name)[0]}"
    markdown = f"# {module_name}\n\n"

    markdown += f"""!!! note "Collection Note"
    This module is part of the __networktocode.nautobot__ collection https://galaxy.ansible.com/networktocode/nautobot (version 5.2.1).

    To install it, use: `ansible-galaxy collection install networktocode.nautobot`.
    You need further requirements to be able to use this module,
    see [Requirements](#requirements) for details.

    To use it in a playbook, specify: `{module_name}`.
"""

    markdown += """\n+++ 1.0.0 "Initial Modules Creation."
    Initial creation of Nautobot modules.\n"""

    if documentation:
        synopsis = extract_synopsis(documentation)
        markdown += f"## Synopsis\n\n- {synopsis}\n\n"

    merged_doc = merge_fragments(documentation, fragments)

    if merged_doc:
        doc_yaml = yaml.safe_load(merged_doc)
        if "requirements" in doc_yaml:
            markdown += "## Requirements\n\n"
            for req in doc_yaml["requirements"]:
                markdown += f"- {req}\n"
            markdown += "\n"
        
        if "options" in doc_yaml:
            markdown += "## Parameters\n\n| Parameter | Data Type | Version Added | Comments |\n| --------- | --------- | ------------- | -------- |\n"
            for param, details in doc_yaml["options"].items():
                data_type = details.get("type", "string")
                version_added = details.get("version_added", "")
                comments = format_description(details.get("description", []), module_name)
                comments = format_multiline(comments)
                markdown += f"| {param} | {data_type} | {version_added} | {comments} |\n"

    markdown += """\n## Tags

!!! note "Note"
    * Tags should be defined as a YAML list
    * This should be ran with connection local and hosts localhost\n\n"""

    if examples:
        # Replace C(code) with `code` and E(env_var) with link in examples
        examples = re.sub(r'C\((.+?)\)', r'`\1`', examples)
        examples = re.sub(r'E\((.+?)\)', lambda m: f"[`{m.group(1)}`](../code_reference/environment_variables.md#{m.group(1).lower()})", examples)
        markdown += "## Examples\n\n```yaml\n" + examples + "\n```\n"

    if return_section:
        markdown += "## Return Values\n\n| Key | Data Type | Description |\n| --- | --------- | ----------- |\n"
        return_pattern = re.compile(r'(\w+):\n  description: (.+)')
        for match in return_pattern.finditer(return_section):
            key = match.group(1)
            desc = match.group(2)
            data_type = "dictionary" if key == "cable" else "string"  # Example data type, update as needed
            description = desc + "<br>Returned: success (when state=present)" if key == "cable" else desc + "<br>Returned: always"
            markdown += f"| {key} | {data_type} | {description} |\n"

    markdown += """\n## Authors

- Tobias Groß (@toerb)\n\n"""

    markdown += """## Collection Links

[Issue Tracker](https://github.com/nautobot/nautobot-ansible/issues/)<br>
[Repository Source](https://github.com/nautobot/nautobot-ansible/)\n"""

    return markdown

def generate_docs(src_dir, dest_dir):
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                documentation = extract_section(content, "DOCUMENTATION")
                examples = extract_section(content, "EXAMPLES")
                return_section = extract_section(content, "RETURN")
                fragments = extract_fragments(content)
                markdown_content = convert_to_markdown(file, documentation, examples, return_section, fragments)
                if markdown_content:
                    relative_path = os.path.relpath(file_path, src_dir)
                    markdown_path = os.path.splitext(relative_path)[0] + ".md"
                    dest_path = os.path.join(dest_dir, markdown_path)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    with open(dest_path, "w") as md_file:
                        md_file.write(markdown_content)
                    print(f"Generated documentation for {file} at {dest_path}")

def generate_env_var_reference(dest_dir):
    env_var_reference_path = os.path.join(dest_dir, "environment_variables.md")
    os.makedirs(os.path.dirname(env_var_reference_path), exist_ok=True)
    
    with open(env_var_reference_path, "w") as ref_file:
        ref_file.write("# Index of All Collection Environment Variables\n\n")
        ref_file.write("The following index documents all environment variables declared by plugins in collections. Environment variables used by the ansible-core configuration are documented in ansible_configuration_settings.\n\n")
        
        for env_var, modules in env_var_usage.items():
            ref_file.write(f"## {env_var.lower()}\n\n")
            ref_file.write(f"See the documentation for the options where this environment variable is used.\n\n")
            module_links = [f"[{module.split('.')[-1]}](../../plugins/{module.split('.')[-1]}/)" for module in modules]
            ref_file.write(f"_Used by_: {', '.join(module_links)}\n\n")

if __name__ == "__main__":
    src_dir = "plugins/modules"  # Update with your actual source directory
    dest_dir = "docs/plugins"  # Update with your desired destination directory
    generate_docs(src_dir, dest_dir)
    environment_variable_dest_dir = "docs/code_reference/"
    generate_env_var_reference(environment_variable_dest_dir)
