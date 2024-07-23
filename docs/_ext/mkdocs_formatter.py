import re

from antsibull_docs_parser.format import Formatter
from antsibull_docs_parser.md import dom
from antsibull_docs_parser.html import _url_escape, html_escape as _html_escape
import typing as t

_CUSTOM_MD_ESCAPE = re.compile(r"""([!"#$%&()*+,:;<=>?@[\\\]^_`{|}~.-])""")


def custom_md_escape(text: str) -> str:
    return _CUSTOM_MD_ESCAPE.sub(r"\\\1", text)


class MkdocsMDFormatter(Formatter):
    @staticmethod
    def _format_option_like(part: t.Union[dom.OptionNamePart, dom.ReturnValuePart], url: t.Optional[str]) -> str:
        link_start = ""
        link_end = ""
        if url:
            link_start = f'<a href="{_html_escape(_url_escape(url))}">'
            link_end = "</a>"
        strong_start = ""
        strong_end = ""
        if part.type == dom.PartType.OPTION_NAME and part.value is None:
            strong_start = "<strong>"
            strong_end = "</strong>"
        if part.value is None:
            text = part.name
        else:
            text = f"{part.name}={part.value}"
        return f"<code>{strong_start}{link_start}{custom_md_escape(text)}{link_end}{strong_end}</code>"

    def format_error(self, part: dom.ErrorPart) -> str:
        return f"<b>ERROR while parsing</b>: {custom_md_escape(part.message)}"

    def format_bold(self, part: dom.BoldPart) -> str:
        return f"<b>{custom_md_escape(part.text)}</b>"

    def format_code(self, part: dom.CodePart) -> str:
        return f"<code>{custom_md_escape(part.text)}</code>"

    def format_horizontal_line(self, part: dom.HorizontalLinePart) -> str:
        return "<hr>"

    def format_italic(self, part: dom.ItalicPart) -> str:
        return f"<em>{custom_md_escape(part.text)}</em>"

    def format_link(self, part: dom.LinkPart) -> str:
        url_escaped = custom_md_escape(_url_escape(part.url))
        return f"[{custom_md_escape(part.text)}]({url_escaped})"

    def format_module(self, part: dom.ModulePart, url: t.Optional[str]) -> str:
        if url:
            return f"[{custom_md_escape(part.fqcn)}]({custom_md_escape(_url_escape(url))})"
        return custom_md_escape(part.fqcn)

    def format_rst_ref(self, part: dom.RSTRefPart) -> str:
        return custom_md_escape(part.text)

    def format_url(self, part: dom.URLPart) -> str:
        url_escaped = custom_md_escape(_url_escape(part.url))
        return f"[{url_escaped}]({url_escaped})"

    def format_text(self, part: dom.TextPart) -> str:
        return custom_md_escape(part.text)

    def format_env_variable(self, part: dom.EnvVariablePart) -> str:
        return f"<code>{custom_md_escape(part.name)}</code>"

    def format_option_name(self, part: dom.OptionNamePart, url: t.Optional[str]) -> str:
        return self._format_option_like(part, url)

    def format_option_value(self, part: dom.OptionValuePart) -> str:
        return f"<code>{custom_md_escape(part.value)}</code>"

    def format_plugin(self, part: dom.PluginPart, url: t.Optional[str]) -> str:
        if url:
            return f"[{custom_md_escape(part.plugin.fqcn)}]({custom_md_escape(_url_escape(url))})"
        return custom_md_escape(part.plugin.fqcn)

    def format_return_value(self, part: dom.ReturnValuePart, url: t.Optional[str]) -> str:
        return self._format_option_like(part, url)


# Default formatter instance
MKDOCS_FORMATTER = MkdocsMDFormatter()
