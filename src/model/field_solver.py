# -*- coding: utf-8 -*-

"""
Esta clase es la encargada de ejecutar los scripts en matlab/octave
correspondientes para resolver los campos
"""

from model.calculation_mode import CalculationMode
from matlab_interface.matlab_interface import MatlabInterface

class FieldSolver(object):

    def __init__(self):

        super(FieldSolver, self).__init__()

        self.matlab_interface = MatlabInterface()

    def solve_field(self, na, nbr, nbi, nc, nz, d, mode):

        # Llama al script en matlab correspondiente y devolver la lista solucion
        # Esta lista contiene dos elementos: [[Re, Im], [Re, Im]]
        complex_solution = None
        if mode == CalculationMode.Parallel:
            complex_solution = self.matlab_interface.solve_field_parallel(na, nbr, nbi, nc, nz, d)
        else:
            complex_solution = self.matlab_interface.solve_field_perpendicular(na, nbr, nbi, nc, nz, d) 

        return [[complex_solution[0].real, complex_solution[0].imag], [complex_solution[1].real, complex_solution[1].imag]] 
