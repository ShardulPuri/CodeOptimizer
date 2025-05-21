from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class OptimizationInfo:
    original_tac: Dict[str, str]
    optimized_tac: Optional[Dict[str, str]] = None
    reason: str = ''

class ConstantPropagator:
    def __init__(self):
        self.constant_map: Dict[str, str] = {}
        self.optimization_log: List[OptimizationInfo] = []

    def _is_numeric(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _update_constant_map(self, lhs: str, arg1: str) -> None:
        if self._is_numeric(arg1):
            self.constant_map[lhs] = arg1
        else:
            # If arg1 is a variable that maps to a constant, propagate that constant
            if arg1 in self.constant_map:
                self.constant_map[lhs] = self.constant_map[arg1]
            else:
                # If arg1 is not a constant or doesn't map to one, remove any previous mapping
                self.constant_map.pop(lhs, None)

    def optimize(self, tac_instructions: List[Dict[str, str]]) -> List[Dict[str, str]]:
        optimized = []
        self.optimization_log.clear()
        self.constant_map.clear()

        for instr in tac_instructions:
            opt_instr = instr.copy()
            
            # Handle simple assignments
            if instr['op'] == '=' and 'arg2' not in instr:
                self._update_constant_map(instr['lhs'], instr['arg1'])
                
                # If we're assigning from a variable that maps to a constant
                if instr['arg1'] in self.constant_map:
                    opt_instr['arg1'] = self.constant_map[instr['arg1']]
                    self.optimization_log.append(
                        OptimizationInfo(
                            original_tac=instr,
                            optimized_tac=opt_instr,
                            reason=f'Propagated constant: {instr["arg1"]} -> {opt_instr["arg1"]}'
                        )
                    )
                    optimized.append(opt_instr)
                    continue
            
            # Handle binary operations
            if 'arg2' in instr:
                # Replace variables with their constant values if available
                if instr['arg1'] in self.constant_map:
                    opt_instr['arg1'] = self.constant_map[instr['arg1']]
                if instr['arg2'] in self.constant_map:
                    opt_instr['arg2'] = self.constant_map[instr['arg2']]
                
                # If both operands are now constants, this will be handled by constant folding
                if opt_instr != instr:
                    self.optimization_log.append(
                        OptimizationInfo(
                            original_tac=instr,
                            optimized_tac=opt_instr,
                            reason='Replaced variables with constant values'
                        )
                    )
                    optimized.append(opt_instr)
                    continue
            
            # If no optimization was possible, keep the original instruction
            optimized.append(instr)
            self.optimization_log.append(OptimizationInfo(original_tac=instr))

        return optimized

    def get_optimization_log(self) -> List[OptimizationInfo]:
        return self.optimization_log