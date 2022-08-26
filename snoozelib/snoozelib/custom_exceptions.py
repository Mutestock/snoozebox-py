class MultipleDataTypesError(Exception):
    pass


class NoSqlDataTypeError(Exception):
    pass


class MissingExpectedValue(Exception):
    pass


class MalformedSequence(Exception):
    pass


class MissingTableInRelations(Exception):
    pass


class RelationsOutsideBounds(Exception):
    pass


class ReservedKeyword(Exception):
    pass


class ManyToManyPrimaryKeyMismatch(Exception):
    pass