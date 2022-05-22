
from snoozelib.import_instruction import ImportInstruction

# https://www.postgresql.org/docs/current/datatype.html
# We're not covering most of these. It's out of scope
data_types = {
    "bigint": [
        "Column(BigInteger)", [
            ImportInstruction("sqlalchemy", "BigInteger"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "int8": [
        "Column(BigInteger)", [
            ImportInstruction("sqlalchemy", "BigInteger"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "bigserial": [
        "Column(BigInteger, primary_key=True, auto_increment=True)", [
            ImportInstruction("sqlalchemy", "BigInteger"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "serial8": [
        "Column(BigInteger, primary_key=True, auto_increment=True)", [
            ImportInstruction("sqlalchemy", "BigInteger"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "bit": (),
    "bit varying(n)": (),
    "varbit(n)": (),
    "boolean": [
        "Column(Boolean)", [
            ImportInstruction("sqlalchemy", "Boolean"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "bool": [
        "Column(Boolean)", [
            ImportInstruction("sqlalchemy", "Boolean"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "box": (),
    "bytea": [
        "Column(LargeBinary)", [
            ImportInstruction("sqlalchemy", "LargeBinary"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "character(n)": [
        "Column(CHAR(n))", [
            ImportInstruction("sqlalchemy", "CHAR"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "char(n)": [
        "Column(CHAR(n))", [
            ImportInstruction("sqlalchemy", "CHAR"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "character varying(n)":  [
        "Column(String(n))", [
            ImportInstruction("sqlalchemy", "String"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "varchar(n)":  [
        "Column(String(n))", [
            ImportInstruction("sqlalchemy", "String"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "cidr": (),
    "circle": (),
    "date":  [
        "Column(Date())", [
            ImportInstruction("sqlalchemy", "Date"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "double precision": [
        "Column(Float(precision=8))", [
            ImportInstruction("sqlalchemy", "Float"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "float8": [
        "Column(Float(precision=8))", [
            ImportInstruction("sqlalchemy", "Float"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "inet": (),
    "integer": [
        "Column(Integer)", [
            ImportInstruction("sqlalchemy", "Integer"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "int": [
        "Column(Integer)", [
            ImportInstruction("sqlalchemy", "Integer"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "int4": [
        "Column(Integer)", [
            ImportInstruction("sqlalchemy", "Integer"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
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
    "real": [
        "Column(Float(precision=4))", [
            ImportInstruction("sqlalchemy", "Float"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "float4": [
        "Column(Float(precision=4))", [
            ImportInstruction("sqlalchemy", "Float"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "smallint": (),
    "int2": (),
    "smallserial": (),
    "serial2": (),
    "serial": [
        "Column(Integer, primary_key=True, autoincrement=True)", [
            ImportInstruction("sqlalchemy", "Integer"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "serial4": (),
    "text": (),
    "time without time zone": [
        "Column(Time(timezone=False))", [
            ImportInstruction("sqlalchemy", "Time"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "time with time zone": [
        "Column(Time(timezone=True))", [
            ImportInstruction("sqlalchemy", "Time"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "timetz": [
        "Column(Time(timezone=True))", [
            ImportInstruction("sqlalchemy", "Time"),
            ImportInstruction("sqlalchemy", "Column")
        ]
    ],
    "timestamp without time zone": [
        "Column(DateTime(timezone=False, server_default=func.now(), onpdate=func.now()))", [
            ImportInstruction("sqlalchemy", "DateTime"),
            ImportInstruction("sqlalchemy", "Column"),
            ImportInstruction("sqlalchemy.sql", "func"),
        ]
    ],
    "timestamp with time zone": [
        "Column(DateTime(timezone=, server_default=func.now(), onpdate=func.now()))", [
            ImportInstruction("sqlalchemy", "DateTime"),
            ImportInstruction("sqlalchemy", "Column"),
            ImportInstruction("sqlalchemy.sql", "func"),
        ]
    ],
    "timestamptz": [
        "Column(DateTime(timezone=, server_default=func.now(), onpdate=func.now()))", [
            ImportInstruction("sqlalchemy", "DateTime"),
            ImportInstruction("sqlalchemy", "Column"),
            ImportInstruction("sqlalchemy.sql", "func"),
        ]
    ],
    "tsquery": (),
    "tsvector": (),
    "txid_snapshot": (),
    "uuid": (),
    "xml": (),
}

