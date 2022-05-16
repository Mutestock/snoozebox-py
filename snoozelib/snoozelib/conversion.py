from dataclasses import dataclass
from typing import List, Optional
from snoozelib.import_instruction import ImportInstruction
import textwrap




@dataclass
class Conversion():
    name: Optional[str] = None
    contents: Optional[str] = None
    import_instructions: Optional[List[ImportInstruction]] = None
    
    
    
    def resolve_contents(self):
        res: str = ""
        instructions_sorted: dict = {}
        for instruction in self.import_instructions:
            if not instruction.origin in instructions_sorted.keys():
                instructions_sorted[instruction.origin] = []
            instructions_sorted[instruction.origin].append(instruction.import_name)
        
        
        # 'value' is a list of import modules here
        for key, value in instructions_sorted.items():
            suffix: str = ", ".join(value)
            res+=f"from {key} import {suffix}"
            
        
            
            
                
            

        
        
        res += textwrap.dedent(f"""\
            class {self.name.capitalize()}(Base):
                __tablename__: str = {self.name.lower()}
                
                
            
            
        """)
        
        
        
    def concatenate_dependencies(self, dependency_list: List[ImportInstruction]):
        for dependency in dependency_list:
            if not self.import_instructions:
                self.import_instructions = [dependency]
            for current_dependency in self.import_instructions:
                if dependency.origin != current_dependency.origin or dependency.import_name != current_dependency.import_name:
                    self.import_instructions.append(dependency)