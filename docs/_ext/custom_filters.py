"""Provides custom filters to pass into Jinja environment."""

from antsibull_docs_parser.md import to_md
from antsibull_docs_parser.parser import Context, parse
from jinja2 import Environment

import re


def convert_text(input_str):
    # Define patterns and replacements
    code_block_pattern = r"C\((.*?)\)"
    italics_pattern = r"I\((.*?)\)"
    bold_pattern = r"B\((.*?)\)"
    environment_pattern = r"E\((.*?)\)"

    # Replace each pattern with the desired output
    converted_str = re.sub(code_block_pattern, r"`\1`", input_str)
    converted_str = re.sub(italics_pattern, r"_\1_", converted_str)
    converted_str = re.sub(bold_pattern, r"__\1__", converted_str)
    converted_str = re.sub(environment_pattern, r"`\1`", converted_str)

    return converted_str


# def parse_docs(text_str, current_plugin=None, role_entrypoint=None):
#     # OLD CODE
#     # context = Context(current_plugin=current_plugin, role_entrypoint=role_entrypoint)
#     # paragraphs = parse(text_str, context, errors="message")
#     # output = to_md(paragraphs)
#     # return output

#     # NEW CODE
#     # Replace I() with italics
#     text_str = text_str.replace("I(", "_")
#     text_str = text_str.replace(")", "_")

#     # Replace B() with bold
#     text_str = text_str.replace("B(", "__")
#     text_str = text_str.replace(")", "__")

#     # Replace C() with code
#     text_str = text_str.replace("C(", "`")
#     text_str = text_str.replace(")", "`")


# Function to add custom filters to a Jinja environment
def add_custom_filters(env: Environment):
    env.filters["convert_text"] = convert_text
