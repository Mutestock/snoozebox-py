from io import TextIOWrapper
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass
from jinja2 import Environment, PackageLoader, select_autoescape


@dataclass
class TemplateFileStructure:
    """Base for for template usage with Jinja.

    :return: Base for template usage with Jinja
    :rtype: TemplateFileStructure
    """

    template_path: Path
    generated_file_path: Path
    jinja_env: Environment
    render_args: Dict

    def get_render(self) -> str:
        """The generated contents from the jinja files after rendering

        :return: Rendered results
        :rtype: str
        """
        return self._filter_render_for_printing(
            self.jinja_env.get_template(self.template_path).render(self.render_args)
        )

    def _filter_render_for_printing(self, to_filter: str) -> str:
        to_filter = to_filter.replace("&#34;", '"')
        return to_filter



def write_templates(template_file_structure: List[TemplateFileStructure]) -> None:
    """Writes templates to the files defined in a list of TemplateFileStructures.

    :param template_file_structure: List of TemplateFileStructures which contain some variables and functions for template generation.
    :type template_file_structure: List[TemplateFileStructure]
    """
    for template_file in template_file_structure:
        file_writer: TextIOWrapper = open(template_file.generated_file_path, "a")
        file_reader: TextIOWrapper = open(template_file.generated_file_path, "r")
        render: str = template_file.get_render()
        current: str = "".join(file_reader.readlines())

        # These two are just for comparing
        stripped_render: str = render.replace(" ", "").rstrip()
        stripped_current: str = current.replace(" ", "").rstrip()

        if not stripped_render in stripped_current:
            file_writer.write(render)



def setup_templating() -> Environment:
    """The loaded templating environment. Sets a variety of configurations.

    :return: Jinja environment with applied configurations.
    :rtype: Environment
    """
    return Environment(loader=PackageLoader("gen"), autoescape=select_autoescape)
