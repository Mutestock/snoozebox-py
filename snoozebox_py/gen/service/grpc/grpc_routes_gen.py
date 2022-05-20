import textwrap
from gen.block_writer_abstract import BlockWriter
from utils.pathing import get_relative_project_src_directory


class GrpcRoutes(BlockWriter):
    def write(self, config: dict) -> None:
        project_directories: dict = config['settings']['file_structure']['project_directories']
        handlers: str = project_directories['handlers'][0]
        routes: str = project_directories['routes'][0]
        service: str = project_directories['service'][0]
        protogen: str = project_directories['protogen'][0]
        logic: str = project_directories['logic'][0]
        
        
        for schematic in config["schematics"]:
            file_writer = open(
                f"{get_relative_project_src_directory(config)}/{service}/{routes}/{schematic.name}.py", "w"
            )

            file_writer.write(
                textwrap.dedent(
                    f"""\
                    from {protogen}.{schematic.name.lower()}_pb2_grpc import {schematic.name.capitalize()}Servicer
                    from {protogen} import {schematic.name.lower()}_pb2
                    from {logic}.{handlers}.{schematic.name.lower()}_handler import {schematic.name.capitalize()}Handler
                    
                    class {schematic.name.capitalize()}Router({schematic.name.capitalize()}Servicer):
                        {schematic.name.lower()}_handler: {schematic.name.capitalize()}Handler = {schematic.name.capitalize()}Handler()
                    
                """
                )
            )

            if "create" in schematic['crud_instructions']:
                file_writer.write(
                    textwrap.dedent(
                        f"""\
                        def Create{schematic.name.capitalize()}(
                            self, request: {schematic.name.lower()}_pb2.Create{schematic.name.capitalize()}Request, _
                        ) -> {schematic.name.lower()}_pb2.Create{schematic.name.capitalize()}Response:
                            return self.{schematic.name.lower()}_handler.create(request)      
                                  
                    """
                    )
                )

            elif "read" in schematic['crud_instructions']:
                file_writer.write(
                    textwrap.dedent(
                        f"""\
                        def Read{schematic.name.capitalize()}(
                            self, request: {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}Request, _
                        ) -> {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}Response:
                            return self.{schematic.name.lower()}_handler.read(request)

                    """
                    )
                )
            elif "update" in schematic['crud_instructions']:
                file_writer.write(
                    textwrap.dedent(
                        f"""\
                        def Update{schematic.name.capitalize()}(
                            self, request: {schematic.name.lower()}_pb2.Update{schematic.name.capitalize()}Request, _
                        ) -> {schematic.name.lower()}_pb2.Update{schematic.name.capitalize()}Response:
                            return self.{schematic.name.lower()}_handler.update(request)
                                  
                    """
                    )
                )
            elif "delete" in schematic['crud_instructions']:
                file_writer.write(
                    textwrap.dedent(
                        f"""\
                        def Delete{schematic.name.capitalize()}(
                            self, request: {schematic.name.lower()}_pb2.Delete{schematic.name.capitalize()}Request, _
                        ) -> {schematic.name.lower()}_pb2.Delete{schematic.name.capitalize()}Request:
                            return self.{schematic.name.lower()}_handler.delete(request)
    
                    """
                    )
                )
            elif "read_list" in schematic['crud_instructions']:
                file_writer.write(
                    textwrap.dedent(
                        f"""\   
                        def Read{schematic.name.capitalize()}List(
                            self, request: {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}ListRequest, _
                        ) -> {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}ListRequest:
                            return self.{schematic.name.lower()}_handler.read_list(request)

                    """
                    )
                )

            file_writer.close()

    def write_test(self, config: dict) -> None:
        pass
