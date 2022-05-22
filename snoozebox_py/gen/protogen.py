from gen.block_writer_abstract import BlockWriter
import textwrap
import subprocess
from pathlib import Path
from pipe import where
from utils.pathing import get_relative_project_root_directory


class ProtogenWriter(BlockWriter):
    def write(self, config: dict) -> None:
        protogen_sh: str = config["settings"]["file_structure"]["project_files"][
            "protogen_file"
        ]
        proto_directory = get_relative_project_root_directory(config) + "/proto"
        if not Path(proto_directory).is_dir():
            Path(proto_directory).mkdir()

        for schematic_file in config["schematics"]:
            for schematic in schematic_file:
                
                def _new_object_name():
                    return f"New{schematic.name.capitalize()}Object new_{schematic.name.lower()}_object"
                
                
                
                file_writer = open(
                    f"{proto_directory}/{schematic.name.lower()}.proto", "w"
                )

                file_writer.write(
                    textwrap.dedent(
                        f"""\
                syntax = "proto3";
                package = {schematic.name.lower()};
                
                service {schematic.name.capitalize()}{{
                """
                    )
                )

                if "create" in config["crud_instructions"]:
                    file_writer.write(
                        f"  rpc Create{schematic.name.capitalize()}(Create{schematic.name.capitalize()}Request) returns (Create{schematic.name.capitalize()}Response) {{}}\n"
                    )

                if "read" in config["crud_instructions"]:
                    file_writer.write(
                        f"  rpc Read{schematic.name.capitalize()}(Read{schematic.name.capitalize()}Request) returns (Read{schematic.name.capitalize()}Response) {{}}\n"
                    )

                if "update" in config["crud_instructions"]:
                    file_writer.write(
                        f"  rpc Update{schematic.name.capitalize()}(Update{schematic.name.capitalize()}Request) returns (Update{schematic.name.capitalize()}Response) {{}}\n"
                    )

                if "delete" in config["crud_instructions"]:
                    file_writer.write(
                        f"  rpc Delete{schematic.name.capitalize()}(Delete{schematic.name.capitalize()}Request) returns (Delete{schematic.name.capitalize()}Response) {{}}\n"
                    )

                if "read_list" in config["crud_instructions"]:
                    file_writer.write(
                        f"  rpc Read{schematic.name.capitalize()}List(Read{schematic.name.capitalize()}ListRequest) returns (Read{schematic.name.capitalize()}ListResponse) {{}}\n"
                    )
                file_writer.write("}\n")
                
                file_writer.write("\n// ===================== Utils ========================\n\n")
                
                file_writer.write(f"message {schematic.name.capitalize()}Object {{\n")
                for i, grpc_variable in enumerate(schematic.grpc_variables):
                    file_writer.write(f"  {grpc_variable.var_type} {grpc_variable.var_name} = {i+1};\n")
                file_writer.write("}\n")
                
                file_writer.write(f"message New{schematic.name.capitalize()}Object {{\n")
                no_default_variables = list( schematic.grpc_variables | where(lambda x: x.default==False))
                for i, grpc_variable in enumerate(no_default_variables):
                    file_writer.write(f"  {grpc_variable.var_type} {grpc_variable.var_name} = {i+1};\n")
                file_writer.write("}\n")
                
                
                file_writer.write("\n// ===================== Request ========================\n\n")
                
                if "create" in config["crud_instructions"]:
                    file_writer.write(f"message Create{schematic.name.capitalize()}Request {{ {_new_object_name()} = 1; }}\n")
                
                if "read" in config["crud_instructions"]:
                    file_writer.write(f"message Read{schematic.name.capitalize()}Request {{ int32 id = 1; }}\n")
                
                if "update" in config["crud_instructions"]:
                    file_writer.write(f"message Update{schematic.name.capitalize()}Request {{\n  int32 id = 1;\n  {_new_object_name()} = 2;\n}}\n")
                
                if "delete" in config["crud_instructions"]:
                    file_writer.write(f"message Delete{schematic.name.capitalize()}Request {{ int32 id = 1; }}\n")
                
                if "read_list" in config["crud_instructions"]:
                    file_writer.write(f"message ReadList{schematic.name.capitalize()}Request{{}}\n")
                
                file_writer.write("\n// ===================== Response ========================\n\n")
                
                                
                if "create" in config["crud_instructions"]:
                    file_writer.write(f"message Create{schematic.name.capitalize()}Response {{ string msg = 1; }}\n")
                
                if "read" in config["crud_instructions"]:
                    file_writer.write(f"message Read{schematic.name.capitalize()}Response {{\n  {_new_object_name()} = 1;\n  string msg = 2;\n}}\n")
                
                if "update" in config["crud_instructions"]:
                    file_writer.write(f"message Update{schematic.name.capitalize()}Response {{\n  int32 id = 1;\n  {_new_object_name()} = 2;\n}}\n")
                
                if "delete" in config["crud_instructions"]:
                    file_writer.write(f"message Delete{schematic.name.capitalize()}Response {{ string msg = 1; }}\n")
                
                if "read_list" in config["crud_instructions"]:
                    file_writer.write(f"message ReadList{schematic.name.capitalize()}Response {{\n  repeated {_new_object_name()} = 1;\n  string msg = 2;\n}}\n")
                
                file_writer.close()
        
        # ==== Protogen.sh  ====
        
        file_writer = open(
            f"{get_relative_project_root_directory(config)}/{protogen_sh}", "w"
        )
        file_writer.write(
            textwrap.dedent(
               f"""\
            #!/bin/bash
            echo "generating gRPC..."
            proto_dir=proto
            for entry in "$proto_dir"/*
            do
                proto_name="$(basename $entry)"
                proto_name="${{proto_name%.*}}"
                echo "found ${{proto_name}}..."
                python -m grpc_tools.protoc -I./proto --python_out=./{config["project_name"]}/protogen --grpc_python_out=./{config["project_name"]}/protogen $entry
                sed -i "s/import ${{proto_name}}_pb2 as ${{proto_name}}__pb2/import protogen.${{proto_name}}_pb2 as ${{proto_name}}__pb2/g" "./{config["project_name"]}/protogen/${{proto_name}}_pb2_grpc.py"
            done

            export AUDIO_ARCHIVER_TESTING=1

            echo "running nose..."
            nose2 -v
            echo "done"           
        """
            )
        )
        file_writer.close()

    def write_test(self, config: dict) -> None:
        pass

    def docker_compose_write(self, config: dict) -> None:
        pass

    def config_write(self, config: dict) -> None:
        pass


def run_protogen(config: dict) -> None:
    relative_project_path = f"services/{config['project_name']}"
    protogen_sh = config["settings"]["file_structure"]["project_files"]["protogen_file"]

    subprocess.run(
        ["chmod", "+x", protogen_sh], check=True, text=True, cwd=relative_project_path
    )
    subprocess.run(["./protogen.sh"], check=True, text=True, cwd=relative_project_path)
