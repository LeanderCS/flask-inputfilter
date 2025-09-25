from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Union

from jinja2 import Environment, FileSystemLoader, StrictUndefined


class TemplateRenderer:
    """Template rendering engine for code generation."""

    def __init__(self, template_dir: Union[str, Path] = None):
        if template_dir is None:
            template_dir = Path(__file__).parent.parent / "templates"

        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        self.env.filters["python_json"] = TemplateRenderer._python_json_filter

    @staticmethod
    def _python_json_filter(value):
        """Convert value to Python-compatible representation."""
        if value is None:
            return "None"
        if value is True:
            return "True"
        if value is False:
            return "False"
        if isinstance(value, str):
            return json.dumps(value)
        if isinstance(value, (int, float)):
            return str(value)
        return json.dumps(value)

    def render_inputfilter(
        self, template_path: str, context: Dict[str, Any]
    ) -> str:
        """Render an InputFilter class from template."""
        template = self.env.get_template(Path(template_path).name)
        return template.render(**context)

    def render_test_file(self, context: Dict[str, Any]) -> str:
        """Render a test file for the generated InputFilter."""
        template = self.env.get_template("test.py.j2")
        return template.render(**context)

    def render_config_file(self, context: Dict[str, Any]) -> str:
        """Render a configuration file template."""
        template = self.env.get_template("config.yaml.j2")
        return template.render(**context)
