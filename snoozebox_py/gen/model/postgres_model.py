import textwrap
from gen.block_writer_abstract import BlockWriter
from utils.pathing import get_relative_project_src_directory


class PostgresModelWriter(BlockWriter):
    def write(self, config: dict) -> None:
        project_directories: dict = config["settings"]["file_structure"][
            "project_directories"
        ]
        models: str = project_directories["models"][0]
        connection: str = project_directories["connection"][0]
        protogen: str = project_directories["protogen"][0]

        schematics = config["schematics"]
        for schematic in schematics:
            file_writer = open(
                f"{get_relative_project_src_directory(config)}/{models}/{schematic.name}.py",
                "w",
            )
            file_writer.write(
                textwrap.dedent(
                    f"""\
                from {connection}.postgres_connection import Base
            """
                )
            )

            if config["service"] == "gRPC":
                file_writer.write(
                    f"from {protogen} import {schematic.name.lower()}_pb2"
                )

            file_writer.write(schematic.contents)

            if config["service"] == "gRPC":

                # Constructor

                file_writer.write(
                    textwrap.dedent(
                        f"""\
                    def __init__(
                        self,
                """
                    )
                )
                for variable_name in schematic.variables_names:
                    file_writer.write(f"        {variable_name}=None,")

                file_writer.write(
                    textwrap.dedent(
                        f"""\
                        grpc_{schematic.name.lower()}_object: {schematic.name.lower()}_pb2.New{schematic.name.capitalize()}Object = None" 
                    ) -> None:
                        if grpc_{schematic.name.lower()}_object:
                """
                    )
                )
                for variable_name in schematic.variable_names:
                    file_writer.write(
                        f"            self.{variable_name} = grpc_{schematic.name.lower()}_channel_object.{variable_name}"
                    )
                file_writer.write("            else:")
                for variable_name in schematic.variable_names:
                    file_writer.write(
                        f"            self.{variable_name}={variable_name}"
                    )

                # to grpc object

                file_writer.write(
                    textwrap.dedent(
                        f"""\
                    def to_grpc_object(self) -> {schematic.name.lower()}_pb2.{schematic.name.capitalize()}Object:
                        return {schematic.name.lower()}_pb2.{schematic.name.capitalize()}Object(
                """
                    )
                )
                for variable_name in schematic.variable_names:
                    file_writer.write(
                        f"              {variable_name}=self.{variable_name}"
                    )
                    
                file_writer.write(")")
                
            file_writer.close()
