# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from utils.multiple_values_entry_parameter import MultipleValuesEntryParameter
from calculation_solution import CalculationSolution

"""
Esta clase es la encargada de ejecutar los scripts en matlab/octave
correspondientes para resolver los calculos
"""

class CalculationSolver(object):

    def __init__(self):

        super(CalculationSolver, self).__init__()

        self.m = MultipleValuesEntryParameter("m")

        self.solution = CalculationSolution()

    def solve_m_parameter(self, na, nbr, nc, d, nz, nbi_min, mode):

        # TODO: Llamar al script en matlab correspondiente y devolver el valor inicial y final de 'm'
        self.m.set_value(1)
        self.m.set_value_to(2)

    def solve_calculation(self):

        # TODO: Llamar al script en matlab correspondiente y devolver la lista de tuplas solucion
        # TODO: Recordar el timeout!
        self.solution.set_solution([(1, 2), (2, 2), (3, 4), (4, 5), (10, 10), (4, 6), (1, 12), (50, 12), (12312312312312, 3), (123, 4)])
