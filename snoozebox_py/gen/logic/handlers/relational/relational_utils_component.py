import textwrap
from gen.block_writer_abstract import BlockWriter
from utils.pathing import get_relative_project_src_directory


class RelationalUtilsComponent(BlockWriter):
    subject: str = "component"

    def write(self, config: dict) -> None:
        project_directories: dict = config['settings']['file_structure']['project_directories']
        logic: str = project_directories['logic'][0]
        handlers: str = project_directories['handlers'][0]
        handler_utils: str = project_directories['handler_utils'][0]
        file_writer = open(
            f"{get_relative_project_src_directory(config)}/{logic}/{handlers}/{handler_utils}/utils_handler_component.py",
            "w",
        )

        file_writer.write(
            textwrap.dedent(
                f"""\
                from sqlalchemy import select
                from sqlalchemy import func


                class UtilsHandlerComponent:
                    def __init__(self, object_instance):
                        self.table = object_instance.__table__

                    def count(self) -> int:
                        return select([func.count()]).select_from(self.table).scalar()      
            """
            )
        )

    def write_test(self, config: dict) -> None:
        pass
