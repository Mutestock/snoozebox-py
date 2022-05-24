from utils.pathing import indent_writer
from gen.block_writer_abstract import BlockWriter
from gen.config_gen import dict_recurse_define
from utils.pathing import get_relative_project_src_directory
from pipe import select


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
            f"{get_relative_project_src_directory(config)}/{service}/grpc_main.py", "w"
        )
        indent_writer(
            lvl=0,
            text=f"""\
                import grpc
                from concurrent import futures
                
                from {utils}.config import CONFIG
                """,
            file_writer=file_writer,
        )
        for schematic_file in schematics:
            for schematic in schematic_file:
                indent_writer(
                    lvl=0,
                    text=f"""\
                    from {protogen}.{schematic.name.lower()}_pb2_grpc import add_{schematic.name.capitalize()}Servicer_to_server                                                                
                    """,
                    file_writer=file_writer,
                )

        for schematic_file in schematics:
            for schematic in schematic_file:
                indent_writer(
                    lvl=0,
                    text=f"""\
                    from {service}.grpc.routes.{schematic.name.lower()}_routes import {schematic.name.capitalize()}Router
                    """,
                    file_writer=file_writer,
                )
            indent_writer(
                lvl=0,
                text=f"""\
                \n
                    def run_grpc() -> None:
                        uri = f"{{CONFIG['grpc']['host']}}:{{CONFIG['grpc']['port']}}"
                        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
                        print(f"GRPC: running on {{uri}}")
                    """,
                file_writer=file_writer,
            )

        for schematic_file in schematics:
            for schematic in schematic_file:

                indent_writer(
                    lvl=4,
                    text=f"add_{schematic.name.capitalize()}Servicer_to_server({schematic.name.capitalize()}Router(), server)\n",
                    file_writer=file_writer,
                )
            indent_writer(
                lvl=4,
                text=f"""
                server.add_insecure_port(uri)
                server.start()
                server.wait_for_termination()\n
                """,
                file_writer=file_writer,
            )

    def write_test(self, config: dict) -> None:
        pass

    def write_config(self, config: dict) -> None:
        def mode_write(config: dict, mode: str) -> None:
            dict_recurse_define(config, ["relative_config_toml", mode, "grpc"])
            config["relative_config_toml"][mode]["grpc"]["host"] = config["settings"][
                "server"
            ]["grpc"]["host"]
            config["relative_config_toml"][mode]["grpc"]["port"] = config["settings"][
                "server"
            ]["grpc"]["port"]

        list(["local", "test"] | select(lambda x: mode_write(config, x)))
