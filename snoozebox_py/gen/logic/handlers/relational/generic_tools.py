


import textwrap
from gen.couple_writer_abstract import CoupleWriter


class RelationalCrudComponent(CoupleWriter):
    subject: str = "component"

    def write(self, config: dict) -> None:
        file_writer = open(
            f"{config.get('handler_path')}/handler_utils/crud_handler_component.py", "w"
        )
        
        file_writer.write(
            textwrap.dedent("""\
                from datetime import datetime
                
                SUCCESFUL_TRANSACTION = "Ok"


                def make_error_message(ex: Exception) -> str:
                    return f"Err {ex}"


                def prepare_object_for_querying(obj: object) -> dict:
                    return {
                        key: value
                        for (key, value) in obj.__dict__.items()
                        if value != None and key != "_sa_instance_state"
                    }

                def iter_parse_datetime(some_dict: dict) -> dict:
                    intermediate = {}
                    for key, value in some_dict.items():
                        if type(value) == datetime:
                            intermediate[key]=str(value)
                        else:
                            intermediate[key]=value
                    return intermediate
            """)
        )
        

    def write_test(self, config: dict) -> None:
        pass
