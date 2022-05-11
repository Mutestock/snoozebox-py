import textwrap
from gen.couple_writer_abstract import CoupleWriter


class GrpcHandler(CoupleWriter):
    subject: str = ""

    def write(self, config: dict) -> None:
        object_name = config.get("object_name")
        file_writer = open(
            f"{config.get('handler_path')}/{object_name}_handler.py", "w"
        )

        file_writer.write(
            textwrap.dedent(
                f"""\
                from logic.handlers.handler_utils.crud_handler_component import (
                    CrudHandlerComponent,
                )
                from logic.handlers.handler_utils.utils_handler_component import (
                    UtilsHandlerComponent,
                )
                from protogen import {object_name.lower()}_pb2
                from logic.handlers.handler_utils.generic_tools import (
                    SUCCESFUL_TRANSACTION,
                    make_error_message,
                )
                from models.{object_name.lower()} import {object_name.capitalize()}
                from pipe import map
                import logging
                
                class {object_name.capitalize()}Handler:
                    def __init__(self):
                        self.object_instance = {object_name.capitalize()}()
                        self.crud_component = CrudHandlerComponent(object_instance=self.object_instance)
                        self.utils_component = UtilsHandlerComponent(object_instance=self.object_instance)
                        
                    def create(
                        self, request: {object_name.lower()}_pb2.Create{object_name.capitalize()}Request
                    ) -> {object_name.lower()}_pb2.Create{object_name.capitalize()}Response:
                        try:
                            self.crud_component.create({object_name.capitalize()}(grpc_{object_name.lower()}_object=request))
                            return {object_name.lower()}_pb2.Create{object_name.capitalize()}Response(msg=SUCCESFUL_TRANSACTION)
                        except Exception as ex:
                            logging.error(
                                f"{object_name.capitalize()} create failed. Error: {{ex}}, type = {{type(ex)}}"
                            )
                            return {object_name.lower()}_pb2.Create{object_name.capitalize()}Response(
                                msg=make_error_message(ex) + " " + str(request)
                            )
                    
                    
                    def read(
                        self, request: {object_name.lower()}_pb2.Read{object_name.capitalize()}Request
                    ) -> {object_name.lower()}_pb2.Read{object_name.capitalize()}Response:
                        {object_name.lower()}: dict = {{}}
                        try:
                            {object_name.lower()} = self.crud_component.read(request.id)
                            return {object_name.lower()}_pb2.Read{object_name.capitalize()}Response(
                                {object_name.lower()}_object={object_name.lower()}, msg=SUCCESFUL_TRANSACTION
                            )
                        except Exception as ex:
                            logging.error(
                                f"{object_name.capitalize()} read failed id: {{request.id}}, Error: {{ex}}, {object_name.lower()} = {{{object_name.capitalize()}}}(), type = {{type(ex)}}"
                            )
                            return {object_name.lower()}_pb2.Read{object_name.capitalize()}Response(msg=make_error_message(ex))
                            
                            
                            
                    def update(
                        self, request: {object_name.lower()}_pb2.Update{object_name.capitalize()}Request
                    ) -> {object_name.lower()}_pb2.Update{object_name.capitalize()}Response:
                        try:
                            {object_name.lower()} = {object_name.capitalize()}(grpc_{object_name.lower()}_object=request[1])
                            self.crud_component.update(id=request[0], obj={object_name.lower()})
                            return {object_name.lower()}_pb2.Update{object_name.capitalize()}Response(msg=SUCCESFUL_TRANSACTION)
                        except Exception as ex:
                            logging.error(
                                f"{object_name.capitalize()} update failed Error: {{ex}}, {object_name.lower()} = {{{object_name.capitalize()}}}(), type = {{type(ex)}}"
                            )
                            return {object_name.lower()}_pb2.Update{object_name.capitalize()}Response(msg=make_error_message(ex))
                            
                            
                    
                    def delete(
                        self, request: {object_name.lower()}_pb2.Delete{object_name.capitalize()}Request
                    ) -> {object_name.lower()}_pb2.Delete{object_name.capitalize()}Response:
                        try:
                            self.crud_component.delete(id=request[0])
                            return {object_name.lower()}_pb2.Delete{object_name.capitalize()}Response(msg=SUCCESFUL_TRANSACTION)
                        except Exception as ex:
                            logging.error(
                                f"{object_name.capitalize()} delete failed id: {{request.id}}, Error: {{ex}}, {object_name.lower()} = {{{object_name.capitalize()}}}(), type = {{type(ex)}}"
                            )
                            return {object_name.lower()}_pb2.Delete{object_name.capitalize()}Response(msg=make_error_message(ex))
                            
                            
                    def read_list(
                        self, _: {object_name.lower()}_pb2.Read{object_name.capitalize()}ListRequest
                    ) -> {object_name.lower()}_pb2.Read{object_name.capitalize()}ListResponse:
                        try:
                            return {object_name.lower()}_pb2.Read{object_name.capitalize()}ListResponse(
                                {object_name.lower()}_objects=self.crud_component.read_list(),
                                msg=SUCCESFUL_TRANSACTION,
                            )
                        except Exception as ex:
                            logging.error(f"{object_name.capitalize()} read list failed: Error: {{ex}}, type: {{type(ex)}}")
                            return {object_name.lower()}_pb2.Read{object_name.capitalize()}ListResponse(msg=make_error_message(ex))
                """
            )
        )

    def write_test(self, config: dict) -> None:
        pass
