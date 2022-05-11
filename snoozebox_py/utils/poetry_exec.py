import subprocess

def run_poetry(config: dict) -> None:
    print(config)
    poetry_new_command = f"poetry new services/{config['project_name']}"
    subprocess.run(["poetry", "new", f"services/{config['project_name']}"], check=True, text=True)
    for dependency in config["collected_dependencies"]:
        subprocess.run(f"poetry add {dependency}")