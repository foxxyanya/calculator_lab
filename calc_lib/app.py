from __future__ import annotations

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout

from calc_lib.operand import Operand, round_operand

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

    def calculate(self):
        try:
            operand_1 = Operand.from_str(self.ids['operand_1'].text)
            operand_2 = Operand.from_str(self.ids['operand_2'].text)

            operator_1 = self._current_operators[0]

            result = self._perform_operation(operand_1, operand_2, operator_1)
            
            self.ids['result_field'].text = str(result.value)
        except Exception as e:
            self.ids['result_field'].text = f'Failed calculating with following error: {e}'

    def _perform_operation(self, lhs: Operand, rhs: Operand, operator: str) -> Operand:
        if operator:
            result = self._operator_handlers[operator](lhs, rhs)
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
