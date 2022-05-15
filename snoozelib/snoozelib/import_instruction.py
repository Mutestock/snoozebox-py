from dataclasses import dataclass

@dataclass
class ImportInstruction():
    origin: str
    import_name: str
    