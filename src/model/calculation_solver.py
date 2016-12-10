# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from utils.multiple_values_entry_parameter import MultipleValuesEntryParameter
from model.calculation_solution import CalculationSolution
from model.calculation_mode import CalculationMode
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

        # Retorna una lista que representa el rango de m
        if mode == CalculationMode.Parallel:
            return self.matlab_interface.solve_m_parallel(na, nbr, nc, d)
        else:
            return self.matlab_interface.solve_m_perpendicular(na, nbr, nc, d) 

    def solve_calculation(self, na, nbr, nc, d_nz):

        # TODO: Recordar el timeout!
        return self.matlab_interface.solve_both(na, nbr, nc, d_nz)
