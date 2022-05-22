import subprocess


def run_poetry(config: dict) -> None:
    relative_project_path = f"services/{config['project_name']}"
    subprocess.run(
        ["poetry", "new", relative_project_path], check=True, text=True
    )
    subprocess.run(["poetry", "add"]+config['collected_dependencies'], check=True, text=True, cwd=relative_project_path)

def poetry_shell(config: dict) -> None:
    relative_project_path = f"services/{config['project_name']}"
    subprocess.run(["poetry", "shell"], check=True, text=True, cwd=relative_project_path)
    