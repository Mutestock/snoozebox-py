
import subprocess
from typing import Dict

def run_protogen(config: Dict) -> None:
    """Executes the generated protogen.sh file. This is only used with gRPC. 
    The purpose of the protogen file is to translate the .proto files to python files recursively with the grpc library.
    
    :param config: Configuration dictionary which gets passed around and modified during the generation process
    :type config: Dict
    """    
    relative_project_path = f"services/{config['project_name']}"
    protogen_sh = config["settings"]["file_structure"]["project_files"]["protogen_file"]

    subprocess.run(
        ["chmod", "+x", protogen_sh], check=True, text=True, cwd=relative_project_path
    )
    subprocess.run(["./protogen.sh"], check=True, text=True, cwd=relative_project_path)
