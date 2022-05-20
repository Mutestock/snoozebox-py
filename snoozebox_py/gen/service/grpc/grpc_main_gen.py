import textwrap
from gen.block_writer_abstract import BlockWriter
from utils.pathing import get_relative_project_src_directory


class Grpc(BlockWriter):
    subject: str = "service"

    def write(self, config: dict) -> None:

        project_directories: dict = config["settings"]["file_structure"][
            "project_directories"
        ]
        service: str = project_directories["service"][0]
        protogen: str = project_directories["protogen"][0]
        utils: str = project_directories["utils"][0]
        schematics: str = config["schematics"]

        file_writer = open(
            f"{get_relative_project_src_directory(config)}/{service}/grpc.py", "w"
        )

        file_writer.write(
            textwrap.dedent(
                f"""\
                import grpc
                from concurrent import futures
                
                from {utils}.config import CONFIG
                """
            )
        )

        for schematic in schematics:
            file_writer.write(
                textwrap.dedent(
                    f"""\
                from {protogen}.{schematic.lower()}_pb2_grpc import add_{schematic.capitalize()}Servicer_to_server                                                                
                """
                )
            )

        for schematic in schematics:
            file_writer.write(
                textwrap.dedent(
                    f"""\
                from {service}.grpc.routes.{schematic}_routes import {schematic.capitalize()}Router
                """
                )
            )

        file_writer.write(
            textwrap.dedent(
                f"""\
            def run_grpc() -> None:
                uri = f"{{CONFIG['grpc']['host']}}:{{CONFIG['grpc']['port']}}"
                server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
                print(f"GRPC: running on {{uri}}")
            """
            )
        )

        for schematic in schematics:
            file_writer.write(
                f"""\
                add_{schematic}Servicer_to_server(AudioRouter(), server)
                """
            )

        file_writer.write(
            textwrap.dedent(
                f"""\
                server.add_insecure_port(uri)
                server.start()
                server.wait_for_termination()
            """
            )
        )

    def write_test(self, config: dict) -> None:
        pass