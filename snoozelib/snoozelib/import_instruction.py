from dataclasses import dataclass
from typing import List

@dataclass
class ImportInstruction():
    origin: str
    import_name: str

@dataclass
class SortedInstruction():
    origin: str
    imports: List[str]
    
    @staticmethod
    def from_import_instruction(import_instruction: ImportInstruction):
        return SortedInstruction(origin=import_instruction.origin, imports=[import_instruction.import_name])