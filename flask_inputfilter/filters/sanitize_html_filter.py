from __future__ import annotations

"""HTML sanitization filter for XSS protection."""

import html
import re
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional

from flask_inputfilter.models import BaseFilter


class SanitizeHtmlFilter(BaseFilter):
    """
    Sanitizes HTML content to prevent XSS attacks.

    This filter removes or escapes potentially dangerous HTML elements and
    attributes while preserving safe formatting.
    """

    DEFAULT_ALLOWED_TAGS = {
        "a",
        "abbr",
        "b",
        "blockquote",
        "br",
        "code",
        "del",
        "em",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "hr",
        "i",
        "ins",
        "li",
        "ol",
        "p",
        "pre",
        "q",
        "s",
        "small",
        "span",
        "strong",
        "sub",
        "sup",
        "u",
        "ul",
        "div",
        "table",
        "thead",
        "tbody",
        "tr",
        "td",
        "th",
        "caption",
        "img",
        "figure",
        "figcaption",
    }

    DEFAULT_ALLOWED_ATTRIBUTES = {
        "a": ["href", "title", "target", "rel"],
        "abbr": ["title"],
        "blockquote": ["cite"],
        "code": ["class"],
        "del": ["datetime"],
        "img": ["src", "alt", "title", "width", "height"],
        "ins": ["datetime"],
        "q": ["cite"],
        "div": ["class", "id"],
        "span": ["class", "id"],
        "table": ["class"],
        "td": ["colspan", "rowspan"],
        "th": ["colspan", "rowspan"],
    }

    DANGEROUS_PROTOCOLS = {
        "javascript:",
        "data:",
        "vbscript:",
        "file:",
        "about:",
        "chrome:",
    }

    EVENT_HANDLERS = {
        "onabort",
        "onblur",
        "onchange",
        "onclick",
        "ondblclick",
        "onerror",
        "onfocus",
        "onkeydown",
        "onkeypress",
        "onkeyup",
        "onload",
        "onmousedown",
        "onmousemove",
        "onmouseout",
        "onmouseover",
        "onmouseup",
        "onreset",
        "onresize",
        "onselect",
        "onsubmit",
        "onunload",
        "onafterprint",
        "onbeforeprint",
        "onbeforeunload",
        "onhashchange",
        "onmessage",
        "onoffline",
        "ononline",
        "onpagehide",
        "onpageshow",
        "onpopstate",
        "onstorage",
        "oncontextmenu",
        "oninput",
        "oninvalid",
        "onsearch",
        "ondrag",
        "ondragend",
        "ondragenter",
        "ondragleave",
        "ondragover",
        "ondragstart",
        "ondrop",
        "onscroll",
        "onwheel",
        "oncopy",
        "oncut",
        "onpaste",
    }

    def __init__(
        self,
        allowed_tags: Optional[set] = None,
        allowed_attributes: Optional[Dict[str, List[str]]] = None,
        strip_tags: bool = False,
        strip_comments: bool = True,
        strip_scripts: bool = True,
        strip_styles: bool = True,
        escape_invalid: bool = True,
        remove_empty: bool = False,
        fix_malformed: bool = True,
        allow_data_urls: bool = False,
    ) -> None:
        """
        Initialize the HTML sanitizer.

        Args:
            allowed_tags: Set of allowed HTML tags
            allowed_attributes: Dict of allowed attributes per tag
            strip_tags: Whether to strip disallowed tags completely
            strip_comments: Whether to remove HTML comments
            strip_scripts: Whether to remove script tags and content
            strip_styles: Whether to remove style tags and attributes
            escape_invalid: Whether to escape invalid HTML
            remove_empty: Whether to remove empty tags
            fix_malformed: Whether to fix malformed HTML
            allow_data_urls: Whether to allow data: URLs
        """
        self.allowed_tags = allowed_tags or self.DEFAULT_ALLOWED_TAGS
        self.allowed_attributes = (
            allowed_attributes or self.DEFAULT_ALLOWED_ATTRIBUTES
        )
        self.strip_tags = strip_tags
        self.strip_comments = strip_comments
        self.strip_scripts = strip_scripts
        self.strip_styles = strip_styles
        self.escape_invalid = escape_invalid
        self.remove_empty = remove_empty
        self.fix_malformed = fix_malformed
        self.allow_data_urls = allow_data_urls

    def apply(self, value: Any) -> str:
        """
        Sanitize the HTML content.

        Args:
            value: The HTML content to sanitize

        Returns:
            Sanitized HTML string
        """
        if value is None:
            return ""

        if not isinstance(value, str):
            value = str(value)

        value = value.replace("\x00", "")

        if self.strip_comments:
            value = re.sub(r"<!--.*?-->", "", value, flags=re.DOTALL)

        if self.strip_scripts:
            value = re.sub(
                r"<script[^>]*>.*?</script>",
                "",
                value,
                flags=re.DOTALL | re.IGNORECASE,
            )
            value = re.sub(r"<script[^>]*>", "", value, flags=re.IGNORECASE)

        if self.strip_styles:
            value = re.sub(
                r"<style[^>]*>.*?</style>",
                "",
                value,
                flags=re.DOTALL | re.IGNORECASE,
            )
            value = re.sub(r"<style[^>]*>", "", value, flags=re.IGNORECASE)

        parser = HTMLSanitizerParser(
            allowed_tags=self.allowed_tags,
            allowed_attributes=self.allowed_attributes,
            strip_tags=self.strip_tags,
            escape_invalid=self.escape_invalid,
            remove_empty=self.remove_empty,
            allow_data_urls=self.allow_data_urls,
            dangerous_protocols=self.DANGEROUS_PROTOCOLS,
            event_handlers=self.EVENT_HANDLERS,
        )

        parser.feed(value)
        result = parser.get_result()

        result = self._additional_xss_protection(result)

        return result

    def _additional_xss_protection(self, html: str) -> str:
        """Apply additional XSS protection measures."""
        html = re.sub(r"javascript:", "", html, flags=re.IGNORECASE)

        for handler in self.EVENT_HANDLERS:
            html = re.sub(
                f"{handler}\\s*=\\s*[\"']?[^\"']*[\"']?",
                "",
                html,
                flags=re.IGNORECASE,
            )

        html = re.sub(
            r"<(\s*)script", "&lt;\\1script", html, flags=re.IGNORECASE
        )
        html = re.sub(
            r"<(\s*)/(\s*)script",
            "&lt;\\1/\\2script",
            html,
            flags=re.IGNORECASE,
        )

        return html


class HTMLSanitizerParser(HTMLParser):
    """HTML parser for sanitization."""

    def __init__(self, **kwargs):
        super().__init__()
        self.allowed_tags = kwargs.get("allowed_tags", set())
        self.allowed_attributes = kwargs.get("allowed_attributes", {})
        self.strip_tags = kwargs.get("strip_tags", False)
        self.escape_invalid = kwargs.get("escape_invalid", True)
        self.remove_empty = kwargs.get("remove_empty", False)
        self.allow_data_urls = kwargs.get("allow_data_urls", False)
        self.dangerous_protocols = kwargs.get("dangerous_protocols", set())
        self.event_handlers = kwargs.get("event_handlers", set())
        self.result = []
        self.tag_stack = []

    def handle_starttag(self, tag, attrs):
        """Handle opening tags."""
        if tag.lower() not in self.allowed_tags:
            if not self.strip_tags and self.escape_invalid:
                self.result.append(html.escape(f"<{tag}>"))
            return

        # Filter attributes
        clean_attrs = []
        allowed_attrs = self.allowed_attributes.get(tag.lower(), [])

        for attr_name, attr_value in attrs:
            # Skip event handlers
            if attr_name.lower() in self.event_handlers:
                continue

            # Skip style attributes if needed
            if attr_name.lower() == "style":
                continue

            # Check if attribute is allowed
            if attr_name.lower() not in allowed_attrs:
                continue

            # Sanitize attribute value
            if attr_name.lower() in ["href", "src", "action"]:
                attr_value = self._sanitize_url(attr_value)
                if attr_value is None:
                    continue

            clean_attrs.append((attr_name, attr_value))

        # Build clean tag
        if clean_attrs:
            attrs_str = " ".join(
                f'{k}="{html.escape(v)}"' for k, v in clean_attrs
            )
            self.result.append(f"<{tag} {attrs_str}>")
        else:
            self.result.append(f"<{tag}>")

        self.tag_stack.append(tag)

    def handle_endtag(self, tag):
        """Handle closing tags."""
        if tag.lower() in self.allowed_tags:
            self.result.append(f"</{tag}>")
            if self.tag_stack and self.tag_stack[-1] == tag:
                self.tag_stack.pop()

    def handle_data(self, data):
        """Handle text data."""
        self.result.append(html.escape(data))

    def _sanitize_url(self, url: str) -> Optional[str]:
        """Sanitize URL to prevent XSS."""
        if not url:
            return None

        url = url.strip()

        # Check for dangerous protocols
        for protocol in self.dangerous_protocols:
            if url.lower().startswith(protocol):
                return None

        # Check for data URLs
        if url.lower().startswith("data:") and not self.allow_data_urls:
            return None

        return url

    def get_result(self) -> str:
        """Get the sanitized HTML."""
        # Close any unclosed tags
        while self.tag_stack:
            tag = self.tag_stack.pop()
            self.result.append(f"</{tag}>")

        return "".join(self.result)
