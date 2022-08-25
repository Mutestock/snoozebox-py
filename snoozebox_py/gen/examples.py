from typing import List
from jinja2 import Environment
from gen.template_file_structure import (
    TemplateFileStructure,
    setup_templating,
    write_templates,
)
from pathlib import Path


def write_examples(path: Path, jinja_env: Environment = None) -> None:
    """Writes a set of example data to append with. It's written during the init phase unless deactivated.

    :param path: The relative path to the schematics directory.
    :type path: Path
    :param jinja_env: The Jinja Environment in which the templates should be written, defaults to None
    :type jinja_env: Environment, optional
    """    
    if not jinja_env:
        jinja_env = setup_templating()
    template_file_structure: List[TemplateFileStructure] = [
        TemplateFileStructure(
            template_path="examples/sql/one_to_many01.sql.jinja",
            generated_file_path=path / "examples/one_to_many01.sql",
            jinja_env=jinja_env,
            render_args={},
        ),
        TemplateFileStructure(
            template_path="examples/sql/one_to_many02.sql.jinja",
            generated_file_path=path / "examples/one_to_many02.sql",
            jinja_env=jinja_env,
            render_args={},
        ),
        TemplateFileStructure(
            template_path="examples/sql/many_to_many01.sql.jinja",
            generated_file_path=path / "examples/many_to_many01.sql",
            jinja_env=jinja_env,
            render_args={},
        ),
        TemplateFileStructure(
            template_path="examples/sql/many_to_many02.sql.jinja",
            generated_file_path=path / "examples/many_to_many02.sql",
            jinja_env=jinja_env,
            render_args={},
        ),
        TemplateFileStructure(
            template_path="examples/sql/many_to_many_association.sql.jinja",
            generated_file_path=path / "examples/many_to_many_association.sql",
            jinja_env=jinja_env,
            render_args={},
        ),
    ]
    write_templates(template_file_structure)
