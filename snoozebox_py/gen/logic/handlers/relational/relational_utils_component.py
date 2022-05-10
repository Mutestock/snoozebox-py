import textwrap
from gen.couple_writer_abstract import CoupleWriter


class RelationalUtilsComponent(CoupleWriter):
    subject: str = "component"

    def write(self, config: dict) -> None:
        file_writer = open(
            f"{config.get('handler_path')}/handler_utils/utils_handler_component.py",
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
