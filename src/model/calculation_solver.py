# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from utils.multiple_values_entry_parameter import MultipleValuesEntryParameter
from model.calculation_solution import CalculationSolution
from matlab_interface.matlab_interface import MatlabInterface

"""
Esta clase es la encargada de ejecutar los scripts en matlab/octave
correspondientes para resolver los calculos
"""

class CalculationSolver(object):

    def __init__(self):

        super(CalculationSolver, self).__init__()

        self.matlab_interface = MatlabInterface()

    def solve_m_parameter(self, na, nbr, nc, d, nz, nbi_min, mode):

        # Retorna una tupla que representa el rango de m
        # TODO: Llamar script de matlab
        return (3, 10)

    def solve_calculation(self, na, nbr, nc, d_nz):

        # TODO: Recordar el timeout!
        return self.matlab_interface.solve_both(na, nbr, nc, d_nz)
