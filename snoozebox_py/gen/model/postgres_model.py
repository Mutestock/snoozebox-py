from utils.pathing import indent_writer
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

        for schematic_file in config["schematics"]:
            for schematic in schematic_file:
                file_writer = open(
                    f"{get_relative_project_src_directory(config)}/{models}/{schematic.name}.py",
                    "w",
                )
                indent_writer(
                    lvl=0,
                    text=f"""
                    from {connection}.postgres_connection import Base
                """,
                    file_writer=file_writer,
                )

                if config["service"] == "gRPC":
                    file_writer.write(
                        f"from {protogen} import {schematic.name.lower()}_pb2\n"
                    )

                file_writer.write(schematic.resolve_contents())

                if config["service"] == "gRPC":

                    # Constructor
                    indent_writer(
                        lvl=4,
                        text=f"""
                        def __init__(
                            self,
                        """,
                        file_writer=file_writer,
                    )
                    for variable_name in schematic.variable_names:
                        indent_writer(
                            lvl=8,
                            text=f"{variable_name} = None,\n",
                            file_writer=file_writer,
                        )
                    indent_writer(
                        lvl=8,
                        text=f"""\
                            grpc_{schematic.name.lower()}_object: {schematic.name.lower()}_pb2.New{schematic.name.capitalize()}Object = None 
                        ) -> None:
                        if grpc_{schematic.name.lower()}_object:
                    """,
                        file_writer=file_writer,
                    )
                    for variable_name in schematic.variable_names:
                        indent_writer(
                            lvl=12,
                            text=f"""\
                            self.{variable_name} = grpc_{schematic.name.lower()}_channel_object.{variable_name},\n
                            """,
                            file_writer=file_writer,
                        )
                    indent_writer(
                        lvl=8,
                        text=f"else:\n",
                        file_writer=file_writer,
                    )
                    for variable_name in schematic.variable_names:
                        indent_writer(
                            lvl=12,
                            text=f"self.{variable_name} = {variable_name},\n",
                            file_writer=file_writer,
                        )

                    # to grpc object

                    indent_writer(
                        lvl=4,
                        text=f"""\
                                \n
                        def to_grpc_object(self) -> {schematic.name.lower()}_pb2.{schematic.name.capitalize()}Object:
                            return {schematic.name.lower()}_pb2.{schematic.name.capitalize()}Object(
                    """,
                        file_writer=file_writer,
                    )
                    for variable_name in schematic.variable_names:
                        indent_writer(
                            lvl=12,
                            text=f"{variable_name}=self.{variable_name},\n",
                            file_writer=file_writer,
                        )

                    indent_writer(
                        lvl=8,
                        text=")",
                        file_writer=file_writer,
                    )

                file_writer.close()
