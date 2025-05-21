from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class OptimizationInfo:
    original_tac: Dict[str, str]
    optimized_tac: Optional[Dict[str, str]] = None
    reason: str = ''

class PeepholeOptimizer:
    def __init__(self):
        self.optimization_log: List[OptimizationInfo] = []

    def _is_numeric(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _simplify_algebraic_identity(self, instr: Dict[str, str]) -> Optional[Dict[str, str]]:
        if 'arg2' not in instr:
            return None

        # x + 0 = x or x - 0 = x
        if (instr['op'] in ['+', '-']) and instr['arg2'] == '0':
            return {
                'lhs': instr['lhs'],
                'op': '=',
                'arg1': instr['arg1']
            }

        # x * 1 = x or x / 1 = x
        if (instr['op'] in ['*', '/']) and instr['arg2'] == '1':
            return {
                'lhs': instr['lhs'],
                'op': '=',
                'arg1': instr['arg1']
            }

        # x * 0 = 0
        if instr['op'] == '*' and (instr['arg1'] == '0' or instr['arg2'] == '0'):
            return {
                'lhs': instr['lhs'],
                'op': '=',
                'arg1': '0'
            }

        return None

    def _simplify_redundant_operations(self, instr: Dict[str, str], prev_instr: Optional[Dict[str, str]]) -> Optional[Dict[str, str]]:
        if not prev_instr:
            return None

        # Check for x = y followed by z = x, convert to z = y
        if (
            prev_instr['op'] == '=' and
            'arg2' not in prev_instr and
            instr['op'] == '=' and
            'arg2' not in instr and
            instr['arg1'] == prev_instr['lhs']
        ):
            return {
                'lhs': instr['lhs'],
                'op': '=',
                'arg1': prev_instr['arg1']
            }

        return None

    def optimize(self, tac_instructions: List[Dict[str, str]]) -> List[Dict[str, str]]:
        optimized = []
        self.optimization_log.clear()
        prev_instr = None

        for instr in tac_instructions:
            # Try algebraic identity simplification
            opt_instr = self._simplify_algebraic_identity(instr)
            if opt_instr:
                self.optimization_log.append(
                    OptimizationInfo(
                        original_tac=instr,
                        optimized_tac=opt_instr,
                        reason='Simplified algebraic identity'
                    )
                )
                optimized.append(opt_instr)
                prev_instr = opt_instr
                continue

            # Try redundant operation elimination
            opt_instr = self._simplify_redundant_operations(instr, prev_instr)
            if opt_instr:
                self.optimization_log.append(
                    OptimizationInfo(
                        original_tac=instr,
                        optimized_tac=opt_instr,
                        reason='Eliminated redundant operation'
                    )
                )
                optimized.append(opt_instr)
                prev_instr = opt_instr
                continue

            # No optimization possible
            optimized.append(instr)
            self.optimization_log.append(OptimizationInfo(original_tac=instr))
            prev_instr = instr

        return optimized

    def get_optimization_log(self) -> List[OptimizationInfo]:
        return self.optimization_log