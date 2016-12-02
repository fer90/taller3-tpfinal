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

    def solve_m_parameter(self, na, nbr, nc, d, nz, nbi_min, mode):

        # Retorna una tupla que representa el rango de m
        # TODO: Llamar script de matlab
        return (3, 10)

    def solve_calculation(self, d_nz, m_from, m_to):

        # TODO: Llamar al script en matlab correspondiente y devolver la lista de tuplas solucion
        # TODO: Recordar el timeout!
        return [(1, 2), (2, 2), (3, 4), (4, 5), (10, 10), (4, 6), (1, 12), (50, 12), (12312312312312, 3), (123, 4)]
