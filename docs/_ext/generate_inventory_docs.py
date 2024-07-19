import os
import ast
import yaml


def extract_documentation(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    try:
        parsed_content = ast.parse(content)
        for node in parsed_content.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "DOCUMENTATION":
                        if isinstance(node.value, (ast.Str, ast.Constant)):  # ast.Str for Python < 3.8, ast.Constant for Python >= 3.8
                            return ast.literal_eval(node.value)
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    return None


def read_inventory_plugins(src_dir):
    documentation_dict = {}
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                file_path = os.path.join(root, file)
                documentation = extract_documentation(file_path)
                if documentation:
                    try:
                        doc_dict = yaml.safe_load(documentation)
                        documentation_dict[file.replace(".py", "")] = doc_dict
                    except yaml.YAMLError as e:
                        print(f"Error parsing YAML in {file}: {e}")
    return documentation_dict


if __name__ == "__main__":
    src_dir = "plugins/inventory"  # Update with your actual source directory for inventory plugins
    docs = read_inventory_plugins(src_dir)
    breakpoint()  # Inspect the `docs` variable here
