import subprocess
from typing import Dict


def run_poetry(config: Dict) -> None:
    """Creates a new poetry project

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    """
    relative_project_path = f"services/{config['project_name']}"
    subprocess.run(["poetry", "new", relative_project_path], check=True, text=True)
    subprocess.run(
        ["poetry", "add"] + config["collected_dependencies"],
        check=True,
        text=True,
        cwd=relative_project_path,
    )


def poetry_shell(config: Dict) -> None:
    """Creates a shell in a poetry project

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    """    
    relative_project_path = f"services/{config['project_name']}"
    subprocess.run(
        ["poetry", "shell"], check=True, text=True, cwd=relative_project_path
    )


def poetry_export_requirements(config: Dict) -> None:
    """Exports the libraries to a requirements.txt files. Necessary because of the generated Dockerfile

    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    """    
    relative_project_path = f"services/{config['project_name']}"
    subprocess.run(
        ["poetry", "export", "-f", "requirements.txt", "--output", "requirements.txt"],
        check=True,
        text=True,
        cwd=relative_project_path,
    )
