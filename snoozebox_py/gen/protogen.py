
import subprocess

def run_protogen(config: dict) -> None:
    relative_project_path = f"services/{config['project_name']}"
    protogen_sh = config["settings"]["file_structure"]["project_files"]["protogen_file"]

    subprocess.run(
        ["chmod", "+x", protogen_sh], check=True, text=True, cwd=relative_project_path
    )
    subprocess.run(["./protogen.sh"], check=True, text=True, cwd=relative_project_path)
