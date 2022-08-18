from dataclasses import dataclass
from typing import List, Optional
from snoozelib.import_instruction import ImportInstruction
from snoozelib.grpc_variable import GrpcVariable

from .import_instruction import SortedInstruction


@dataclass
class Conversion:
    name: Optional[str] = None
    contents: Optional[List[str]] = None
    import_instructions: Optional[List[ImportInstruction]] = None
    sorted_import_instructions: Optional[List[SortedInstruction]] = None
    variable_names: Optional[str] = None
    grpc_variables: Optional[GrpcVariable] = None

    def concatenate_dependencies(self, dependency_list: List[ImportInstruction]):
        for dependency in dependency_list:
            if not self.import_instructions:
                self.import_instructions = [dependency]
            for current_dependency in self.import_instructions:
                if (
                    dependency.origin != current_dependency.origin
                    or dependency.import_name != current_dependency.import_name
                ):
                    self.import_instructions.append(dependency)
                    
    def _rinse_import_instructions(self):
        del self.import_instructions

    def finalize_sorted_instructions(self) -> None:
        for instruction in self.import_instructions:
            hit: bool = False
            if not self.sorted_import_instructions:
                self.sorted_import_instructions = [
                    SortedInstruction.from_import_instruction(instruction)
                ]
                continue
            for sorted_instruction in self.sorted_import_instructions:
                if (
                    sorted_instruction.origin == instruction.origin
                ):
                    if instruction.import_name not in sorted_instruction.imports:
                        sorted_instruction.imports.append(instruction.import_name)
                    hit = True
                    continue
            if hit:
                continue

            else:
                self.sorted_import_instructions.append(
                    SortedInstruction.from_import_instruction(instruction)
                )
        self._rinse_import_instructions()
