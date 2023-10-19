from __future__ import annotations
from typing import Union
import re
import math

class Operand:
    def __init__(self, value: Union[int, float], op_type: str):
        self.value = value
        self.op_type = op_type
    
    def __add__(self, other: Operand) -> Operand:
        return Operand(
            value=self.value + other.value,
            op_type='float' if float in [self.op_type, self.op_type] else 'int' 
        )

    def __mul__(self, other: Operand) -> Operand:
        return Operand(
            value=self.value * other.value,
            op_type='float' if float in [self.op_type, self.op_type] else 'int' 
        )
    
    def __sub__(self, other: Operand) -> Operand:
        return Operand(
            value=self.value - other.value,
            op_type='float' if float in [self.op_type, self.op_type] else 'int' 
        )
    
    def __truediv__(self, other: Operand) -> Operand:
        return Operand(
            value=self.value / other.value,
            op_type='float' if float in [self.op_type, self.op_type] else 'int' 
        )
    
    def __format__(self, __format_spec: str) -> str:
        return format(self.value, __format_spec)
    
    def __str__(self):
        return f"{self.value:,.6f}".replace(",", " ").rstrip('0').rstrip('.') #rstrips to avoiding trailing zeros
    
    @staticmethod
    def validate_operator_str(operand_str: str):
        err_msg = f'Incorrent operant format {operand_str}'

        if not bool(re.match(r'^[\d ,.]+$', operand_str)):
            raise Exception(err_msg + 'with incorrect symbols')
        

        delimeter = None

        if '.' in operand_str:
            delimeter = '.'
        elif ',' in operand_str:
            delimeter = ','

        triples = []

        if delimeter:
            lhs, rhs = operand_str.split(delimeter)

            triples.extend(lhs.split(' ')[1: ])
            triples.extend(rhs.split(' ')[:-1])
        else:
            operand = operand_str.split(' ')
            triples.extend(operand[1:])

        if (all(len(triple) == 3 for triple in triples)):
            return
        else:
            raise Exception(err_msg + 'with incorrect length of triples')
    
    @classmethod
    def from_str(cls, operand_str: str) -> Operand:
        negative = False
        if operand_str[0] == '-':
            negative=True
            operand_str = operand_str[1:]

        Operand.validate_operator_str(operand_str)
        
        op_type=int

        operand_str = operand_str.replace(' ', '')
        if '.' in operand_str or ',' in operand_str:
            operand_str = operand_str.replace(',', '.')
            op_type=float

        return cls(
            value=op_type(operand_str) * (1 if not negative else -1),
            op_type=op_type
        )
    
def round_to_int(operand: Operand, type: str, *args) -> Operand:
    if operand.op_type == float:
        if type == 'math':
            return Operand(
                value=int(operand.value + (0.5 if operand.value > 0 else -0.5)),
                op_type=operand.op_type
            )
        elif type == 'bank':
            return Operand(
                value=round(operand.value),
                op_type=operand.op_type
            )
        elif type == 'floor':
            return Operand(
                value=math.floor(operand.value),
                op_type=operand.op_type
            )
    
    return operand
