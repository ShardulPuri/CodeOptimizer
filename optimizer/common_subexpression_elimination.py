from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class OptimizationInfo:
    original_tac: Dict[str, str]
    optimized_tac: Optional[Dict[str, str]] = None
    reason: str = ''

class CommonSubexpressionEliminator:
    def __init__(self):
        self.optimization_log: List[OptimizationInfo] = []
        self.expression_map: Dict[Tuple[str, str, str], str] = {}

    def _get_expression_key(self, instr: Dict[str, str]) -> Optional[Tuple[str, str, str]]:
        if 'arg2' in instr and instr['op'] != '=':
            return (instr['op'], instr['arg1'], instr['arg2'])
        return None

    def _is_expression_valid(self, key: Tuple[str, str, str], var: str) -> bool:
        # Check if the variables in the expression are not modified
        arg1, arg2 = key[1], key[2]
        return not (self._is_variable_modified(arg1) or self._is_variable_modified(arg2))

    def _is_variable_modified(self, var: str) -> bool:
        # In a basic implementation, we conservatively assume variables might be modified
        # A more sophisticated implementation would track variable modifications
        try:
            float(var)
            return False  # Constants are never modified
        except ValueError:
            return True  # Variables might be modified

    def optimize(self, tac_instructions: List[Dict[str, str]]) -> List[Dict[str, str]]:
        optimized = []
        self.optimization_log.clear()
        self.expression_map.clear()

        for instr in tac_instructions:
            expr_key = self._get_expression_key(instr)
            
            if expr_key is not None:
                # Check if we've seen this expression before
                if expr_key in self.expression_map and self._is_expression_valid(expr_key, self.expression_map[expr_key]):
                    # Reuse the previous result
                    opt_instr = {
                        'lhs': instr['lhs'],
                        'op': '=',
                        'arg1': self.expression_map[expr_key]
                    }
                    self.optimization_log.append(
                        OptimizationInfo(
                            original_tac=instr,
                            optimized_tac=opt_instr,
                            reason=f'Reused common subexpression: {expr_key[1]} {expr_key[0]} {expr_key[2]} -> {self.expression_map[expr_key]}'
                        )
                    )
                    optimized.append(opt_instr)
                else:
                    # New expression, store it
                    self.expression_map[expr_key] = instr['lhs']
                    optimized.append(instr)
                    self.optimization_log.append(OptimizationInfo(original_tac=instr))
            else:
                # For assignments and other operations, clear affected expressions
                if 'lhs' in instr:
                    # Remove expressions that use the modified variable
                    self.expression_map = {
                        k: v for k, v in self.expression_map.items()
                        if k[1] != instr['lhs'] and k[2] != instr['lhs']
                    }
                optimized.append(instr)
                self.optimization_log.append(OptimizationInfo(original_tac=instr))

        return optimized

    def get_optimization_log(self) -> List[OptimizationInfo]:
        return self.optimization_log