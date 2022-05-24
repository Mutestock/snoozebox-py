from utils.pathing import indent_writer
from gen.block_writer_abstract import BlockWriter
from utils.pathing import get_relative_project_src_directory


class GrpcRoutes(BlockWriter):
    def write(self, config: dict) -> None:
        project_directories: dict = config["settings"]["file_structure"][
            "project_directories"
        ]
        handlers: str = project_directories["handlers"][0]
        routes: str = project_directories["routes"][0]
        service: str = project_directories["service"][0]
        protogen: str = project_directories["protogen"][0]
        logic: str = project_directories["logic"][0]

        for schematic_file in config["schematics"]:
            for schematic in schematic_file:
                file_writer = open(
                    f"{get_relative_project_src_directory(config)}/{service}/{routes}/{schematic.name}_routes.py",
                    "w",
                )

                indent_writer(
                    lvl=0,
                    text=f"""\
                        from {protogen}.{schematic.name.lower()}_pb2_grpc import {schematic.name.capitalize()}Servicer
                        from {protogen} import {schematic.name.lower()}_pb2
                        from {logic}.{handlers}.{schematic.name.lower()}_handler import {schematic.name.capitalize()}Handler
                        

                        class {schematic.name.capitalize()}Router({schematic.name.capitalize()}Servicer):
                            {schematic.name.lower()}_handler: {schematic.name.capitalize()}Handler = {schematic.name.capitalize()}Handler()
                    """,
                    file_writer=file_writer,
                )

                if "create" in config["crud_instructions"]:
                    indent_writer(
                        lvl=4,
                        text=f"""
                            def Create{schematic.name.capitalize()}(
                                self, request: {schematic.name.lower()}_pb2.Create{schematic.name.capitalize()}Request, _
                            ) -> {schematic.name.lower()}_pb2.Create{schematic.name.capitalize()}Response:
                                return self.{schematic.name.lower()}_handler.create(request)      
                        """,
                        file_writer=file_writer,
                    )

                if "read" in config["crud_instructions"]:
                    indent_writer(
                        lvl=4,
                        text=f"""
                            def Read{schematic.name.capitalize()}(
                                self, request: {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}Request, _
                            ) -> {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}Response:
                                return self.{schematic.name.lower()}_handler.read(request)
                        """,
                        file_writer=file_writer,
                    )
                if "update" in config["crud_instructions"]:
                    indent_writer(
                        lvl=4,
                        text=f"""
                            def Update{schematic.name.capitalize()}(
                                self, request: {schematic.name.lower()}_pb2.Update{schematic.name.capitalize()}Request, _
                            ) -> {schematic.name.lower()}_pb2.Update{schematic.name.capitalize()}Response:
                                return self.{schematic.name.lower()}_handler.update(request)
                        """,
                        file_writer=file_writer,
                    )

                if "delete" in config["crud_instructions"]:
                    indent_writer(
                        lvl=4,
                        text=f"""
                            def Delete{schematic.name.capitalize()}(
                                self, request: {schematic.name.lower()}_pb2.Delete{schematic.name.capitalize()}Request, _
                            ) -> {schematic.name.lower()}_pb2.Delete{schematic.name.capitalize()}Request:
                                return self.{schematic.name.lower()}_handler.delete(request)
                        """,
                        file_writer=file_writer,
                    )

                if "read_list" in config["crud_instructions"]:
                    indent_writer(
                        lvl=4,
                        text=f"""
                            def Read{schematic.name.capitalize()}List(
                                self, request: {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}ListRequest, _
                            ) -> {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}ListRequest:
                                return self.{schematic.name.lower()}_handler.read_list(request)
                        """,
                        file_writer=file_writer,
                    )

                file_writer.close()

    def write_test(self, config: dict) -> None:
        pass
