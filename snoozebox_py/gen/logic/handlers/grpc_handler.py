import textwrap
from gen.block_writer_abstract import BlockWriter
from utils.pathing import get_relative_project_src_directory


class GrpcHandler(BlockWriter):
    subject: str = ""

    def write(self, config: dict) -> None:
        
        project_directories: dict = config['settings']['file_structure']['project_directories']
        logic: str = project_directories['logic'][0]
        handlers: str = project_directories['handlers'][0]
        handler_utils: str = project_directories['handler_utils'][0]
        models: str = project_directories['models'][0]
        protogen: str = project_directories['protogen'][0]
        
        for obj in config["objects"]:
            file_writer = open(
                 f"{get_relative_project_src_directory(config)}/{handlers}/{obj.name}_handler.py",
                "w",
            )

            file_writer.write(
                textwrap.dedent(
                    f"""\
                    from {logic}.{handlers}.{handler_utils}.crud_handler_component import (
                        CrudHandlerComponent,
                    )
                    from {logic}.{handlers}.{handler_utils}.utils_handler_component import (
                        UtilsHandlerComponent,
                    )
                    from {protogen} import {obj.name.lower()}_pb2
                    from {logic}.{handlers}.{handler_utils}.generic_tools import (
                        SUCCESFUL_TRANSACTION,
                        make_error_message,
                    )
                    from {models}.{obj.name.lower()} import {obj.name.capitalize()}
                    from pipe import map
                    import logging

                    class {obj.name.capitalize()}Handler:
                        def __init__(self):
                            self.object_instance = {obj.name.capitalize()}()
                            self.crud_component = CrudHandlerComponent(object_instance=self.object_instance)
                            self.utils_component = UtilsHandlerComponent(object_instance=self.object_instance)
                    """
                )
            )
            if "create" in obj["crud_instructions"]:
                file_writer.write(
                    textwrap.dedent(
                        f"""\
                        def create(
                            self, request: {obj.name.lower()}_pb2.Create{obj.name.capitalize()}Request
                        ) -> {obj.name.lower()}_pb2.Create{obj.name.capitalize()}Response:
                            try:
                                self.crud_component.create({obj.name.capitalize()}(grpc_{obj.name.lower()}_object=request))
                                return {obj.name.lower()}_pb2.Create{obj.name.capitalize()}Response(msg=SUCCESFUL_TRANSACTION)
                            except Exception as ex:
                                logging.error(
                                    f"{obj.name.capitalize()} create failed. Error: {{ex}}, type = {{type(ex)}}"
                                )
                                return {obj.name.lower()}_pb2.Create{obj.name.capitalize()}Response(
                                    msg=make_error_message(ex) + " " + str(request)
                                )
                                
                    """
                    )
                )
            elif "read" in obj["crud_instructions"]:
                file_writer.write(
                    textwrap.dedent(
                        f"""\
                        def read(
                            self, request: {obj.name.lower()}_pb2.Read{obj.name.capitalize()}Request
                        ) -> {obj.name.lower()}_pb2.Read{obj.name.capitalize()}Response:
                            {obj.name.lower()}: dict = {{}}
                            try:
                                {obj.name.lower()} = self.crud_component.read(request.id)
                                return {obj.name.lower()}_pb2.Read{obj.name.capitalize()}Response(
                                    {obj.name.lower()}_object={obj.name.lower()}, msg=SUCCESFUL_TRANSACTION
                                )
                            except Exception as ex:
                                logging.error(
                                    f"{obj.name.capitalize()} read failed id: {{request.id}}, Error: {{ex}}, {obj.name.lower()} = {{{obj.name.capitalize()}}}(), type = {{type(ex)}}"
                                )
                                return {obj.name.lower()}_pb2.Read{obj.name.capitalize()}Response(msg=make_error_message(ex))
                    
                        """
                    )
                )
            elif "update" in obj["crud_instructions"]:
                file_writer.write(
                    textwrap.dedent(
                        f"""\
                        def update(
                            self, request: {obj.name.lower()}_pb2.Update{obj.name.capitalize()}Request
                        ) -> {obj.name.lower()}_pb2.Update{obj.name.capitalize()}Response:
                            try:
                                {obj.name.lower()} = {obj.name.capitalize()}(grpc_{obj.name.lower()}_object=request[1])
                                self.crud_component.update(id=request[0], obj={obj.name.lower()})
                                return {obj.name.lower()}_pb2.Update{obj.name.capitalize()}Response(msg=SUCCESFUL_TRANSACTION)
                            except Exception as ex:
                                logging.error(
                                    f"{obj.name.capitalize()} update failed Error: {{ex}}, {obj.name.lower()} = {{{obj.name.capitalize()}}}(), type = {{type(ex)}}"
                                )
                                return {obj.name.lower()}_pb2.Update{obj.name.capitalize()}Response(msg=make_error_message(ex))
                        """
                    )
                )
            elif "delete" in obj["crud_instructions"]:
                file_writer.write(
                    textwrap.dedent(
                        f"""\
                        def delete(
                            self, request: {obj.name.lower()}_pb2.Delete{obj.name.capitalize()}Request
                        ) -> {obj.name.lower()}_pb2.Delete{obj.name.capitalize()}Response:
                            try:
                                self.crud_component.delete(id=request[0])
                                return {obj.name.lower()}_pb2.Delete{obj.name.capitalize()}Response(msg=SUCCESFUL_TRANSACTION)
                            except Exception as ex:
                                logging.error(
                                    f"{obj.name.capitalize()} delete failed id: {{request.id}}, Error: {{ex}}, {obj.name.lower()} = {{{obj.name.capitalize()}}}(), type = {{type(ex)}}"
                                )
                                return {obj.name.lower()}_pb2.Delete{obj.name.capitalize()}Response(msg=make_error_message(ex))

                        """
                    )
                )
            elif "delete" in obj["crud_instructions"]:
                file_writer.write(
                    textwrap.dedent(
                        f"""\
                        def read_list(
                            self, _: {obj.name.lower()}_pb2.Read{obj.name.capitalize()}ListRequest
                        ) -> {obj.name.lower()}_pb2.Read{obj.name.capitalize()}ListResponse:
                            try:
                                return {obj.name.lower()}_pb2.Read{obj.name.capitalize()}ListResponse(
                                    {obj.name.lower()}_objects=self.crud_component.read_list(),
                                    msg=SUCCESFUL_TRANSACTION,
                                )
                            except Exception as ex:
                                logging.error(f"{obj.name.capitalize()} read list failed: Error: {{ex}}, type: {{type(ex)}}")
                                return {obj.name.lower()}_pb2.Read{obj.name.capitalize()}ListResponse(msg=make_error_message(ex))
                                
                        """
                    )
                )

    def write_test(self, config: dict) -> None:
        pass
