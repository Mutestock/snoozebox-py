from dataclasses import dataclass
from snoozelib.general import get_data_type


@dataclass
class GrpcVariable():
    var_name: str
    var_type: str
    default: bool
    
    
def determine_type_for_grpc(sql_line: str) -> str:
    dtype = get_data_type(sql_line)
    if dtype in [
        "bigint",
        "int8",
        "bigserial",
        "serial8",
        "bit",
        "bit_varying",
        "bytea",
        "double precision",
        "float8",
        "integer",
        "int",
        "int4",
        "real",
        "float4",
        "smallint",
        "int2",
        "smallserial",
        "serial2",
        "serial",
        "serial4",
    ]:
        return "int32"
    elif dtype in ["bool", "boolean"]:
        return "bool"
    else:
        return "string"