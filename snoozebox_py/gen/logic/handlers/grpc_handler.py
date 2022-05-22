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
        
        for schematic_file in config["schematics"]:
            for schematic in schematic_file:
                file_writer = open(
                     f"{get_relative_project_src_directory(config)}/{handlers}/{schematic.name}_handler.py",
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
                        from {protogen} import {schematic.name.lower()}_pb2
                        from {logic}.{handlers}.{handler_utils}.generic_tools import (
                            SUCCESFUL_TRANSACTION,
                            make_error_message,
                        )
                        from {models}.{schematic.name.lower()} import {schematic.name.capitalize()}
                        from pipe import map
                        import logging

                        class {schematic.name.capitalize()}Handler:
                            def __init__(self):
                                self.object_instance = {schematic.name.capitalize()}()
                                self.crud_component = CrudHandlerComponent(object_instance=self.object_instance)
                                self.utils_component = UtilsHandlerComponent(object_instance=self.object_instance)
                        """
                    )
                )
                if "create" in config["crud_instructions"]:
                    file_writer.write(
                        textwrap.dedent(
                            f"""\
                            def create(
                                self, request: {schematic.name.lower()}_pb2.Create{schematic.name.capitalize()}Request
                            ) -> {schematic.name.lower()}_pb2.Create{schematic.name.capitalize()}Response:
                                try:
                                    self.crud_component.create({schematic.name.capitalize()}(grpc_{schematic.name.lower()}_object=request))
                                    return {schematic.name.lower()}_pb2.Create{schematic.name.capitalize()}Response(msg=SUCCESFUL_TRANSACTION)
                                except Exception as ex:
                                    logging.error(
                                        f"{schematic.name.capitalize()} create failed. Error: {{ex}}, type = {{type(ex)}}"
                                    )
                                    return {schematic.name.lower()}_pb2.Create{schematic.name.capitalize()}Response(
                                        msg=make_error_message(ex) + " " + str(request)
                                    )

                        """
                        )
                    )
                if "read" in config["crud_instructions"]:
                    file_writer.write(
                        textwrap.dedent(
                            f"""\
                            def read(
                                self, request: {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}Request
                            ) -> {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}Response:
                                {schematic.name.lower()}: dict = {{}}
                                try:
                                    {schematic.name.lower()} = self.crud_component.read(request.id)
                                    return {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}Response(
                                        {schematic.name.lower()}_schematicect={schematic.name.lower()}, msg=SUCCESFUL_TRANSACTION
                                    )
                                except Exception as ex:
                                    logging.error(
                                        f"{schematic.name.capitalize()} read failed id: {{request.id}}, Error: {{ex}}, {schematic.name.lower()} = {{{schematic.name.capitalize()}}}(), type = {{type(ex)}}"
                                    )
                                    return {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}Response(msg=make_error_message(ex))

                            """
                        )
                    )
                if "update" in config["crud_instructions"]:
                    file_writer.write(
                        textwrap.dedent(
                            f"""\
                            def update(
                                self, request: {schematic.name.lower()}_pb2.Update{schematic.name.capitalize()}Request
                            ) -> {schematic.name.lower()}_pb2.Update{schematic.name.capitalize()}Response:
                                try:
                                    {schematic.name.lower()} = {schematic.name.capitalize()}(grpc_{schematic.name.lower()}_schematicect=request[1])
                                    self.crud_component.update(id=request[0], schematic={schematic.name.lower()})
                                    return {schematic.name.lower()}_pb2.Update{schematic.name.capitalize()}Response(msg=SUCCESFUL_TRANSACTION)
                                except Exception as ex:
                                    logging.error(
                                        f"{schematic.name.capitalize()} update failed Error: {{ex}}, {schematic.name.lower()} = {{{schematic.name.capitalize()}}}(), type = {{type(ex)}}"
                                    )
                                    return {schematic.name.lower()}_pb2.Update{schematic.name.capitalize()}Response(msg=make_error_message(ex))
                            """
                        )
                    )
                if "delete" in config["crud_instructions"]:
                    file_writer.write(
                        textwrap.dedent(
                            f"""\
                            def delete(
                                self, request: {schematic.name.lower()}_pb2.Delete{schematic.name.capitalize()}Request
                            ) -> {schematic.name.lower()}_pb2.Delete{schematic.name.capitalize()}Response:
                                try:
                                    self.crud_component.delete(id=request[0])
                                    return {schematic.name.lower()}_pb2.Delete{schematic.name.capitalize()}Response(msg=SUCCESFUL_TRANSACTION)
                                except Exception as ex:
                                    logging.error(
                                        f"{schematic.name.capitalize()} delete failed id: {{request.id}}, Error: {{ex}}, {schematic.name.lower()} = {{{schematic.name.capitalize()}}}(), type = {{type(ex)}}"
                                    )
                                    return {schematic.name.lower()}_pb2.Delete{schematic.name.capitalize()}Response(msg=make_error_message(ex))

                            """
                        )
                    )
                if "read_list" in config["crud_instructions"]:
                    file_writer.write(
                        textwrap.dedent(
                            f"""\
                            def read_list(
                                self, _: {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}ListRequest
                            ) -> {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}ListResponse:
                                try:
                                    return {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}ListResponse(
                                        {schematic.name.lower()}_schematicects=self.crud_component.read_list(),
                                        msg=SUCCESFUL_TRANSACTION,
                                    )
                                except Exception as ex:
                                    logging.error(f"{schematic.name.capitalize()} read list failed: Error: {{ex}}, type: {{type(ex)}}")
                                    return {schematic.name.lower()}_pb2.Read{schematic.name.capitalize()}ListResponse(msg=make_error_message(ex))

                            """
                        )
                    )

    def write_test(self, config: dict) -> None:
        pass
