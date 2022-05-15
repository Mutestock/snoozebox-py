from typing import Dict, List
from import_instruction import ImportInstruction

# https://www.postgresql.org/docs/current/datatype.html
# We're not covering most of these. It's out of scope
data_types: Dict[str, List[str, List[ImportInstruction]]] = {
    "bigint": [
        "Column(BigInteger)", [
            ImportInstruction("sqlalchemy.types", "BigInteger"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "int8": [
        "Column(BigInteger)", [
            ImportInstruction("sqlalchemy.types", "BigInteger"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "bigserial": [
        "Column(BigInteger, primary_key=True, auto_increment=True)", [
            ImportInstruction("sqlalchemy.types", "BigInteger"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "serial8": [
        "Column(BigInteger, primary_key=True, auto_increment=True)", [
            ImportInstruction("sqlalchemy.types", "BigInteger"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "bit ": (),
    "bit varying [ (n) ]": (),
    "varbit [ (n) ]": (),
    "boolean": [
        "Column(Boolean)", [
            ImportInstruction("sqlalchemy.types", "Boolean"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "bool": [
        "Column(Boolean)", [
            ImportInstruction("sqlalchemy.types", "Boolean"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "box": (),
    "bytea": [
        "Column(LargeBinary)", [
            ImportInstruction("sqlalchemy.types","LargeBinary"),
            ImportInstruction("sqlalchemy", "Column")
        ]    
    ],
    "character(n)": ,
    "char(n)": (),
    "character varying(n)": (),
    "varchar(n)": (),
    "cidr": (),
    "circle": (),
    "date": (),
    "double precision": (),
    "float8": (),
    "inet": (),
    "integer": (),
    "int": (),
    "int4": (),
    "interval [ fields ] [ (p) ]": (),
    "json": (),
    "jsonb": (),
    "line": (),
    "lseg": (),
    "macaddr": (),
    "macaddr8": (),
    "money": (),
    "numeric [ (p, s) ]": (),
    "decimal [ (p, s) ]": (),
    "path": (),
    "pg_lsn": (),
    "pg_snapshot": (),
    "point": (),
    "polygon": (),
    "real	": (),
    "float4": (),
    "smallint": (),
    "int2": (),
    "smallserial": (),
    "serial2": (),
    "serial": (),
    "serial4": (),
    "text": (),
    "time [ (p) ] [ without time zone ]": (),
    "time [ (p) ] with time zone	": (),
    "timetz": (),
    "timestamp [ (p) ] [ without time zone ]": (),
    "timestamp [ (p) ] with time zone": (),
    "timestamptz": (),
    "tsquery": (),
    "tsvector": (),
    "txid_snapshot": (),
    "uuid": (),
    "xml": (),
}
