from typing import Dict, List, Optional, Set
from dataclasses import dataclass

@dataclass
class OptimizationInfo:
    original_tac: Dict[str, str]
    optimized_tac: Optional[Dict[str, str]] = None
    reason: str = ''

class DeadCodeEliminator:
    def __init__(self):
        self.optimization_log: List[OptimizationInfo] = []
        self.used_variables: Set[str] = set()
        self.defined_variables: Dict[str, List[int]] = {}

    def _mark_used_variables(self, instr: Dict[str, str], idx: int) -> None:
        # Mark variables used in arguments
        if 'arg1' in instr and not self._is_numeric(instr['arg1']):
            self.used_variables.add(instr['arg1'])
        if 'arg2' in instr and not self._is_numeric(instr['arg2']):
            self.used_variables.add(instr['arg2'])
        
        # Record variable definitions
        if 'lhs' in instr:
            if instr['lhs'] not in self.defined_variables:
                self.defined_variables[instr['lhs']] = []
            self.defined_variables[instr['lhs']].append(idx)

    def _is_numeric(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _is_critical_instruction(self, instr: Dict[str, str]) -> bool:
        # Instructions that must be preserved (e.g., function calls, I/O operations)
        critical_ops = {'call', 'return', 'print', 'input', 'goto', 'if', 'label'}
        return instr['op'] in critical_ops

    def optimize(self, tac_instructions: List[Dict[str, str]]) -> List[Dict[str, str]]:
        self.optimization_log.clear()
        self.used_variables.clear()
        self.defined_variables.clear()
        
        # First pass: Mark all used variables and collect definitions
        for idx, instr in enumerate(tac_instructions):
            if self._is_critical_instruction(instr):
                self._mark_used_variables(instr, idx)
                if 'lhs' in instr:
                    self.used_variables.add(instr['lhs'])
            else:
                self._mark_used_variables(instr, idx)

        # Second pass: Eliminate dead code
        optimized = []
        for idx, instr in enumerate(tac_instructions):
            if self._is_critical_instruction(instr):
                # Keep all critical instructions
                optimized.append(instr)
                self.optimization_log.append(
                    OptimizationInfo(
                        original_tac=instr,
                        optimized_tac=instr,
                        reason='Critical instruction preserved'
                    )
                )
            elif 'lhs' in instr and instr['lhs'] not in self.used_variables:
                # Skip instructions that define unused variables
                self.optimization_log.append(
                    OptimizationInfo(
                        original_tac=instr,
                        reason=f'Eliminated dead code: variable {instr["lhs"]} is never used'
                    )
                )
            else:
                # Keep instructions with used variables
                optimized.append(instr)
                self.optimization_log.append(
                    OptimizationInfo(
                        original_tac=instr,
                        optimized_tac=instr,
                        reason='Instruction uses live variables'
                    )
                )

        return optimized

    def get_optimization_log(self) -> List[OptimizationInfo]:
        return self.optimization_log