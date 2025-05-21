from typing import Dict, List, Optional, Set
from dataclasses import dataclass

@dataclass
class OptimizationInfo:
    original_tac: Dict[str, str]
    optimized_tac: Optional[Dict[str, str]] = None
    reason: str = ''

class CopyPropagator:
    def __init__(self):
        self.optimization_log: List[OptimizationInfo] = []
        self.copy_map: Dict[str, str] = {}
        self.modified_variables: Set[str] = set()

    def _is_copy_instruction(self, instr: Dict[str, str]) -> bool:
        return (
            'op' in instr and
            instr['op'] == '=' and
            'arg2' not in instr and
            not self._is_numeric(instr['arg1'])
        )

    def _is_numeric(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _update_copy_map(self, lhs: str, rhs: str) -> None:
        # If rhs is already mapped, use its mapping
        actual_rhs = self.copy_map.get(rhs, rhs)
        self.copy_map[lhs] = actual_rhs

    def _invalidate_copies(self, var: str) -> None:
        # Remove all mappings that use the modified variable
        invalid_copies = [
            v for v, mapped in self.copy_map.items()
            if mapped == var
        ]
        for v in invalid_copies:
            self.copy_map.pop(v)

    def optimize(self, tac_instructions: List[Dict[str, str]]) -> List[Dict[str, str]]:
        self.optimization_log.clear()
        self.copy_map.clear()
        self.modified_variables.clear()

        optimized = []
        for instr in tac_instructions:
            if self._is_copy_instruction(instr):
                # Handle copy instruction
                lhs, rhs = instr['lhs'], instr['arg1']
                self._update_copy_map(lhs, rhs)

                # If we can propagate a copy
                if rhs in self.copy_map:
                    opt_instr = instr.copy()
                    opt_instr['arg1'] = self.copy_map[rhs]
                    optimized.append(opt_instr)
                    self.optimization_log.append(
                        OptimizationInfo(
                            original_tac=instr,
                            optimized_tac=opt_instr,
                            reason=f'Propagated copy: {rhs} -> {self.copy_map[rhs]}'
                        )
                    )
                    continue

            # For non-copy instructions
            if 'lhs' in instr:
                # Variable is being modified, invalidate copies
                self._invalidate_copies(instr['lhs'])
                self.modified_variables.add(instr['lhs'])

            # Try to propagate copies in arguments
            opt_instr = instr.copy()
            modified = False

            if 'arg1' in instr and instr['arg1'] in self.copy_map:
                opt_instr['arg1'] = self.copy_map[instr['arg1']]
                modified = True

            if 'arg2' in instr and instr['arg2'] in self.copy_map:
                opt_instr['arg2'] = self.copy_map[instr['arg2']]
                modified = True

            if modified:
                optimized.append(opt_instr)
                self.optimization_log.append(
                    OptimizationInfo(
                        original_tac=instr,
                        optimized_tac=opt_instr,
                        reason='Propagated copied variables in expression'
                    )
                )
            else:
                optimized.append(instr)
                self.optimization_log.append(OptimizationInfo(original_tac=instr))

        return optimized

    def get_optimization_log(self) -> List[OptimizationInfo]:
        return self.optimization_log