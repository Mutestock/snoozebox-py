from dataclasses import dataclass
from typing import List
from import_instruction import ImportInstruction


@dataclass
class Conversion():
    contents: str
    import_instructions: List[ImportInstruction]
    