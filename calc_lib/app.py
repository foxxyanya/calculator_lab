from __future__ import annotations
from typing import Optional

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout

from calc_lib.operand import Operand, round_to_int

Builder.load_file('calc_lib/app_design.kv')

class Interface(AnchorLayout):
    def __init__(self):
        super(Interface, self).__init__()
        self._current_operators = ['+', '+', '+']
        self._operator_handlers = {
            '+': lambda lhs, rhs: lhs + rhs,
            '-': lambda lhs, rhs: lhs - rhs,
            '*': lambda lhs, rhs: lhs * rhs,
            '/': lambda lhs, rhs: lhs / rhs,
        }
        self._round_strategy = 'math'
        self.operations_presicion = 10

    def calculate(self):
        try:
            operand_1 = Operand.from_str(self.ids['operand_1'].text)
            operand_2 = Operand.from_str(self.ids['operand_2'].text)
            operand_3 = Operand.from_str(self.ids['operand_3'].text)
            operand_4 = Operand.from_str(self.ids['operand_4'].text)

            operator_1 = self._current_operators[0]
            operator_2 = self._current_operators[1]
            operator_3 = self._current_operators[2]


            bracket_result = self._perform_operation(operand_2, operand_3, operator_2, self.operations_presicion)

            if operator_1 in ['*', '/'] or operator_3 in ['+', '-']:
                tmp_result = self._perform_operation(operand_1, bracket_result, operator_1, self.operations_presicion)
                result = self._perform_operation(tmp_result, operand_4, operator_3, self.operations_presicion)
            else:
                tmp_result = self._perform_operation(bracket_result, operand_4, operator_3, self.operations_presicion)
                result = self._perform_operation(operand_1, tmp_result, operator_1, self.operations_presicion)

            if self._round_strategy:
                result = round_to_int(result, self._round_strategy)
            
            self.ids['result_field'].text = str(result.value)
        except Exception as e:
            self.ids['result_field'].text = f'Failed calculating with following error: {e}'

    def _perform_operation(self, lhs: Operand, rhs: Operand, operator: str, precision: Optional[float]) -> Operand:
        if operator:
            result: Operand = self._operator_handlers[operator](lhs, rhs)
            if precision:
                result.value = round(result.value, precision)
        else:
            raise Exception("Operator isn't setted")
    
        if abs(result.value) > 1e12:
            raise Exception('Result overflow')
        
        return result
    
    def _set_operator(self, instance, operator: str,  operator_index: int):
        self._current_operators[operator_index] = operator

    def _set_round_strategy(self, instance, round_strategy: str):
        self._round_strategy = round_strategy
   

class CalculatorApp(App):
    def build(self):
        return Interface()
