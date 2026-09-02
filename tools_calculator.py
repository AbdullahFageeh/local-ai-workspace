"""
title: Math & Formula Calculator
author: open-webui-community
description: Accurately calculate complex math, algebra, calculus, and scientific formulas using SymPy.
version: 1.0.0
license: MIT
"""

import sympy
from typing import Any

class Tools:
    def __init__(self):
        pass

    def calculate(self, expression: str) -> str:
        """
        Evaluate and solve mathematical expressions, equations, integrals, or numeric calculations safely.
        :param expression: Mathematical expression or formula to evaluate (e.g. '2**10', 'sqrt(144) * 3', 'solve(x**2 - 4, x)').
        :return: The exact calculated result.
        """
        try:
            # Parse and evaluate mathematical expression with SymPy
            res = sympy.sympify(expression)
            if hasattr(res, 'evalf'):
                numeric = res.evalf()
                return f"Exact Result: {res}\nNumeric Approximation: {numeric}"
            return f"Result: {res}"
        except Exception as e:
            return f"Calculation error: {str(e)}"
