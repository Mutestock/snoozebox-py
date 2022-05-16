from dataclasses import dataclass
from typing import List
from snoozelib.import_instruction import ImportInstruction


@dataclass
class Conversion():
    name: str
    contents: str
    import_instructions: List[ImportInstruction]
    