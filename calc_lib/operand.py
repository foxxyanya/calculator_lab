from __future__ import annotations
from typing import Union
import re
import math
from decimal import Decimal

class Operand:
    def __init__(self, value: Decimal, precision: int = 6):
        self.value = value
        self.precision = precision

    def __add__(self, other: Operand) -> Operand:
        return Operand(
            value=self.value + other.value,
        )

    def __mul__(self, other: Operand) -> Operand:
        return Operand(
            value=self.value * other.value,
        )
    
    def __sub__(self, other: Operand) -> Operand:
        return Operand(
            value=self.value - other.value,
        )
    
    def __truediv__(self, other: Operand) -> Operand:
        return Operand(
            value=self.value / other.value,
        )

    def __str__(self):
        has_fraq_part = (self.value % 1) != 0
        
        if has_fraq_part:
            return f"{self.value:,.6f}".replace(",", " ").rstrip('0').rstrip('.') #rstrips to avoiding trailing zeros
        
        return str(self.value)

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
        
        operand_str = operand_str.replace(' ', '')
        if '.' in operand_str or ',' in operand_str:
            operand_str = operand_str.replace(',', '.')

        return cls(
            value=Decimal(('-' if negative else '') + operand_str)
        )
    
def round_to_int(operand: Operand, type: str) -> Operand:
    if type == 'math':
        return Operand(
            value=int(operand.value + (Decimal(0.5) if operand.value > 0 else Decimal(-0.5))),
        )
    elif type == 'bank':
        return Operand(
            value=round(operand.value)
        )
    elif type == 'floor':
        return Operand(
            value=math.floor(operand.value)
        )
    else:
        return operand