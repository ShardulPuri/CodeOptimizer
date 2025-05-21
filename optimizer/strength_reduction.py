from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class OptimizationInfo:
    original_tac: Dict[str, str]
    optimized_tac: Optional[Dict[str, str]] = None
    reason: str = ''

class StrengthReducer:
    def __init__(self):
        self.optimization_log: List[OptimizationInfo] = []

    def _is_power_of_two(self, value: str) -> Optional[int]:
        try:
            num = float(value)
            if num.is_integer() and num > 0:
                num = int(num)
                if num & (num - 1) == 0:  # Check if number is power of 2
                    return num.bit_length() - 1  # Return the power (e.g., 8 -> 3 because 2^3 = 8)
        except ValueError:
            pass
        return None

    def _can_reduce_multiplication(self, instr: Dict[str, str]) -> bool:
        return (
            instr['op'] == '*' and
            ('arg2' in instr) and
            (self._is_power_of_two(instr['arg1']) is not None or
             self._is_power_of_two(instr['arg2']) is not None)
        )

    def _can_reduce_division(self, instr: Dict[str, str]) -> bool:
        return (
            instr['op'] == '/' and
            'arg2' in instr and
            self._is_power_of_two(instr['arg2']) is not None
        )

    def optimize(self, tac_instructions: List[Dict[str, str]]) -> List[Dict[str, str]]:
        optimized = []
        self.optimization_log.clear()

        for instr in tac_instructions:
            if self._can_reduce_multiplication(instr):
                # Convert multiplication by power of 2 to left shift
                power = self._is_power_of_two(instr['arg2'])
                if power is None:
                    # If arg2 is not power of 2, check arg1
                    power = self._is_power_of_two(instr['arg1'])
                    shift_arg = instr['arg2']
                else:
                    shift_arg = instr['arg1']

                opt_instr = {
                    'lhs': instr['lhs'],
                    'op': '<<',
                    'arg1': shift_arg,
                    'arg2': str(power)
                }
                self.optimization_log.append(
                    OptimizationInfo(
                        original_tac=instr,
                        optimized_tac=opt_instr,
                        reason=f'Reduced multiplication by {2**power} to left shift by {power}'
                    )
                )
                optimized.append(opt_instr)

            elif self._can_reduce_division(instr):
                # Convert division by power of 2 to right shift
                power = self._is_power_of_two(instr['arg2'])
                opt_instr = {
                    'lhs': instr['lhs'],
                    'op': '>>',
                    'arg1': instr['arg1'],
                    'arg2': str(power)
                }
                self.optimization_log.append(
                    OptimizationInfo(
                        original_tac=instr,
                        optimized_tac=opt_instr,
                        reason=f'Reduced division by {2**power} to right shift by {power}'
                    )
                )
                optimized.append(opt_instr)

            else:
                optimized.append(instr)
                self.optimization_log.append(OptimizationInfo(original_tac=instr))

        return optimized

    def get_optimization_log(self) -> List[OptimizationInfo]:
        return self.optimization_log