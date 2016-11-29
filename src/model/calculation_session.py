# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from enum import Enum

from model.calculation_solver import CalculationSolver
from model.m_container import MContainer
from utils.entry_parameter import EntryParameter
from utils.multiple_values_entry_parameter import MultipleValuesEntryParameter

"""
Esta clase representa el modelo de una sesion de calculo.
Se encarga de mantener los datos de una sesion, como asi tambien de ejecutar 
el calculo de la solucion y actualizar la vista con ello (patron Observer)
"""

class CalculationMode(Enum):
    Parallel = 1
    Perpendicular = 2

class CalculationSession(object):

    def __init__(self, load_file = None):

        if load_file is not None:

            # Cargo el modelo desde un archivo guardado
            pass

        else:

            # Cargo un modelo nuevo
            self.initialize_parameters()

    def initialize_parameters(self):

        # Parametros de entrada iniciales
        self.na = EntryParameter("Na")
        self.nbr = EntryParameter("Nbr")
        self.nc = EntryParameter("Nc")
        self.nbi_min = EntryParameter("Nbi")

        # Parametro de entrada elegido
        self.d = MultipleValuesEntryParameter("d'")
        self.nz = MultipleValuesEntryParameter("nz")

        # Modo de ejecucion del calculo
        self.calculation_mode = CalculationMode.Parallel

        # Contenedor de el/los parametro(s) 'm'
        self.m = MContainer()

        # Solucion de m y del calculo
        self.calculation_solver = CalculationSolver()

    def calcule_m_parameter(self, na, nbr, nc, d, nz, nbi_min, mode):

        m_solution = []

        # TODO: Setear todos los parametros
        self.d = d
        
        for d_value in range(d.get_value_from(), d.get_value_to(), d.get_value_step()):

            current_m_solution = []

            current_m_solution.append(d_value)

            m_range = self.calculation_solver.solve_m_parameter(na, nbr, nc, d, nz, nbi_min, mode)

            # TODO: Encapsular rango de m en una clase
            current_m_solution.append(m_range[0])
            current_m_solution.append(m_range[1])

            m_solution.append(current_m_solution)

        self.m.set_parameters(m_solution)

    def calcule_solution(self, m_from, m_to):

        # TODO: Ver parametros que se necesitan
        self.calculation_solver.solve_calculation()

    def save_session(self, filename):
        # TODO: Implementar
        pass

    # Metodos para registrar observadores de parametros
    def register_m_observer(self, observer):

        self.m.register(observer)

    def register_solution_observer(self, observer):

        self.calculation_solver.register_solution_observer(observer)
