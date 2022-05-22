from dataclasses import dataclass


@dataclass
class GrpcVariable():
    var_name: str
    var_type: str
    default: bool