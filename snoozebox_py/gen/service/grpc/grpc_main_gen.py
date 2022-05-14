import textwrap
from gen.couple_writer_abstract import BlockWriter


class Grpc(BlockWriter):
    subject: str = "service"

    def write(self, config: dict) -> None:
        file_writer = open(f"{config.get('service_path')}/grpc.py", "w")

        schematics = config["schematics"]

        file_writer.write(
            textwrap.dedent(
                f"""\
                import grpc
                from concurrent import futures
                
                from utils.config import CONFIG
            """
            )
        )

        for schematic in schematics:
            file_writer.write(
                textwrap.dedent(
                    f"""\
                from protogen.{schematic.lower()}_pb2_grpc import add_{schematic.capitalize()}Servicer_to_server                                                                
            """
                )
            )

        for schematic in schematics:
            file_writer.write(
                textwrap.dedent(
                    f"""\
                from service.grpc.routes.{schematic}_routes import {schematic.capitalize()}Router
            """
                )
            )

        file_writer.write(
            textwrap.dedent(
                """/
            def run_grpc() -> None:
                uri = f"{CONFIG.get('grpc').get('host')}:{CONFIG.get('grpc').get('port')}"
                server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
                print(f"GRPC: running on {uri}")
                add_AudioServicer_to_server(AudioRouter(), server)
                add_ChannelServicer_to_server(ChannelRouter(), server)
                server.add_insecure_port(uri)
                server.start()
                server.wait_for_termination()
        """
            )
        )

    def write_test(self, config: dict) -> None:
        pass
