from typing import List, Dict, Any
import operator
from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class OptimizationInfo:
    original_tac: Dict[str, str]
    optimized_tac: Optional[Dict[str, str]] = None
    reason: str = ''

class ConstantFolder:
    def __init__(self):
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '%': operator.mod,
            '<<': operator.lshift,
            '>>': operator.rshift,
            '&': operator.and_,
            '|': operator.or_,
            '^': operator.xor
        }
        self.optimization_log: List[OptimizationInfo] = []

    def _is_numeric(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _evaluate_constant(self, op: str, arg1: str, arg2: str) -> Optional[str]:
        if op not in self.operators:
            return None
        
        try:
            val1 = float(arg1)
            val2 = float(arg2)
            result = self.operators[op](val1, val2)
            return str(int(result) if result.is_integer() else result)
        except (ValueError, ZeroDivisionError):
            return None

    def optimize(self, tac_instructions: List[Dict[str, str]]) -> List[Dict[str, str]]:
        optimized = []
        self.optimization_log.clear()

        for instr in tac_instructions:
            if 'arg2' in instr and instr['op'] in self.operators:
                if self._is_numeric(instr['arg1']) and self._is_numeric(instr['arg2']):
                    result = self._evaluate_constant(instr['op'], instr['arg1'], instr['arg2'])
                    if result is not None:
                        opt_instr = {
                            'lhs': instr['lhs'],
                            'op': '=',
                            'arg1': result
                        }
                        self.optimization_log.append(
                            OptimizationInfo(
                                original_tac=instr,
                                optimized_tac=opt_instr,
                                reason=f'Folded constant expression: {instr["arg1"]} {instr["op"]} {instr["arg2"]} = {result}'
                            )
                        )
                        optimized.append(opt_instr)
                        continue
            
            optimized.append(instr)
            self.optimization_log.append(OptimizationInfo(original_tac=instr))

        return optimized

    def get_optimization_log(self) -> List[OptimizationInfo]:
        return self.optimization_log