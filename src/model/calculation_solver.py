# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from utils.multiple_values_entry_parameter import MultipleValuesEntryParameter
from model.calculation_solution import CalculationSolution

"""
Esta clase es la encargada de ejecutar los scripts en matlab/octave
correspondientes para resolver los calculos
"""

class CalculationSolver(object):

    def __init__(self):

        super(CalculationSolver, self).__init__()

        self.solution = CalculationSolution()

    def solve_m_parameter(self, na, nbr, nc, d, nz, nbi_min, mode):

        # Retorna una tupla que representa el rango de m
        # TODO: Llamar script de matlab
        return (3, 10)

    def solve_calculation(self):

        # TODO: Llamar al script en matlab correspondiente y devolver la lista de tuplas solucion
        # TODO: Recordar el timeout!
        self.solution.set_solution([(1, 2), (2, 2), (3, 4), (4, 5), (10, 10), (4, 6), (1, 12), (50, 12), (12312312312312, 3), (123, 4)])

    # Metodos para registrar observadores de parametros
    def register_m_from_observer(self, observer):

        self.m.register_from_observer(observer)

    def register_m_to_observer(self, observer):

        self.m.register_to_observer(observer)

    def register_solution_observer(self, observer):

        self.solution.register(observer)
