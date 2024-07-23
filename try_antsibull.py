"""Testing out antsibull-docs-parser."""

from antsibull_docs_parser.format import Formatter
from antsibull_docs_parser.md import to_md
from antsibull_docs_parser.parser import Context, parse

from docs._ext.mkdocs_formatter import MkdocsMDFormatter

text_str = "By default, I(follow_redirects) is set to uses urllib2 default behavior. With an env var E(NAUTOBOT_TOKEN)"

current_plugin = None  # "networktocode.nautobot.inventory"
role_entrypoint = None
context = Context(current_plugin=current_plugin, role_entrypoint=role_entrypoint)
paragraphs = parse(text_str, context, errors="message")
breakpoint()

output = to_md(paragraphs, formatter=MkdocsMDFormatter)
print(output)
