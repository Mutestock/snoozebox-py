import textwrap
from gen.block_writer_abstract import BlockWriter
from utils.pathing import get_relative_project_src_directory


class GenericRelationalTools(BlockWriter):
    subject: str = "component"

    def write(self, config: dict) -> None:
        
        project_directories: dict = config['settings']['file_structure']['project_directories']
        logic: str = project_directories["logic"][0]
        handlers: str = project_directories['handlers'][0]
        handler_utils: str = project_directories['handler_utils'][0]
        
        file_writer = open(
            f"{get_relative_project_src_directory(config)}/{logic}/{handlers}/{handler_utils}/generic_tools.py", "w"
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
