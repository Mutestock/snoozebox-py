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
        
        
        for obj in config["objects"]:
            file_writer = open(
                f"{get_relative_project_src_directory(config)}/{service}/{routes}/{obj.name}.py", "w"
            )

            file_writer.write(
                textwrap.dedent(
                    f"""\
                    from {protogen}.{obj.name.lower()}_pb2_grpc import {obj.name.capitalize()}Servicer
                    from {protogen} import {obj.name.lower()}_pb2
                    from {logic}.{handlers}.{obj.name.lower()}_handler import {obj.name.capitalize()}Handler
                    
                    class {obj.name.capitalize()}Router({obj.name.capitalize()}Servicer):
                        {obj.name.lower()}_handler: {obj.name.capitalize()}Handler = {obj.name.capitalize()}Handler()
                    
                """
                )
            )

            if "create" in obj['crud_instructions']:
                file_writer.write(
                    textwrap.dedent(
                        f"""\
                        def Create{obj.name.capitalize()}(
                            self, request: {obj.name.lower()}_pb2.Create{obj.name.capitalize()}Request, _
                        ) -> {obj.name.lower()}_pb2.Create{obj.name.capitalize()}Response:
                            return self.{obj.name.lower()}_handler.create(request)      
                                  
                    """
                    )
                )

            elif "read" in obj['crud_instructions']:
                file_writer.write(
                    textwrap.dedent(
                        f"""\
                        def Read{obj.name.capitalize()}(
                            self, request: {obj.name.lower()}_pb2.Read{obj.name.capitalize()}Request, _
                        ) -> {obj.name.lower()}_pb2.Read{obj.name.capitalize()}Response:
                            return self.{obj.name.lower()}_handler.read(request)

                    """
                    )
                )
            elif "update" in obj['crud_instructions']:
                file_writer.write(
                    textwrap.dedent(
                        f"""\
                        def Update{obj.name.capitalize()}(
                            self, request: {obj.name.lower()}_pb2.Update{obj.name.capitalize()}Request, _
                        ) -> {obj.name.lower()}_pb2.Update{obj.name.capitalize()}Response:
                            return self.{obj.name.lower()}_handler.update(request)
                                  
                    """
                    )
                )
            elif "delete" in obj['crud_instructions']:
                file_writer.write(
                    textwrap.dedent(
                        f"""\
                        def Delete{obj.name.capitalize()}(
                            self, request: {obj.name.lower()}_pb2.Delete{obj.name.capitalize()}Request, _
                        ) -> {obj.name.lower()}_pb2.Delete{obj.name.capitalize()}Request:
                            return self.{obj.name.lower()}_handler.delete(request)
    
                    """
                    )
                )
            elif "read_list" in obj['crud_instructions']:
                file_writer.write(
                    textwrap.dedent(
                        f"""\   
                        def Read{obj.name.capitalize()}List(
                            self, request: {obj.name.lower()}_pb2.Read{obj.name.capitalize()}ListRequest, _
                        ) -> {obj.name.lower()}_pb2.Read{obj.name.capitalize()}ListRequest:
                            return self.{obj.name.lower()}_handler.read_list(request)

                    """
                    )
                )

            file_writer.close()

    def write_test(self, config: dict) -> None:
        pass
