# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from model.calculation_solver import CalculationSolver
from model.m_container import MContainer
from model.solution_container import SolutionContainer
from model.calculation_mode import CalculationMode
from utils.entry_parameter import EntryParameter
from utils.multiple_values_entry_parameter import MultipleValuesEntryParameter

"""
Esta clase representa el modelo de una sesion de calculo.
Se encarga de mantener los datos de una sesion, como asi tambien de ejecutar 
el calculo de la solucion y actualizar la vista con ello (patron Observer)
"""

class CalculationSession(object):

    def __init__(self, load_file = None):

        if load_file is not None:

            # Cargo el modelo desde un archivo guardado
            self.load_from_file(load_file)

        else:

            # Cargo un modelo nuevo
            self.initialize_parameters()

    def load_from_file(self, filename):

        # TODO: Ver que el archivo exista
        # TODO: Parsear archivo
        # TODO: Setear parametros
        self.d = MultipleValuesEntryParameter("d'", 2, 2, 10)

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
        self.solution = SolutionContainer()

        # Resolvedor de todos los calculos (ifaz hacia matlab)
        self.calculation_solver = CalculationSolver()

    def calcule_m_parameter(self, na, nbr, nc, d, nz, nbi_min, mode):

        m_solution = []

        # TODO: Setear todos los parametros
        self.d = d
        
        for d_value in range(d.get_value_from(), d.get_value_to(), d.get_value_step()):

            current_m_solution = []

            current_m_solution.append(d_value)

            m_range = self.calculation_solver.solve_m_parameter(na, nbr, nc, d_value, nz, nbi_min, mode)

            # FIXME: Encapsular rango de m en una clase
            current_m_solution.append(m_range[0])
            current_m_solution.append(m_range[1])

            m_solution.append(current_m_solution)

        self.m.set_parameters(m_solution)

    def calcule_solution(self, na, nbr, nc, d_m_values, calculation_mode):

        final_solution = []

        for current_calculation in d_m_values:

            current_solution = []

            d_nz = current_calculation[0]
            m_from = current_calculation[1]
            m_to = current_calculation[2]

            current_solution.append(d_nz)

            pair_solution = self.calculation_solver.solve_calculation(na, nbr, nc, d_nz, m_from, m_to, calculation_mode)

            current_solution.append(pair_solution)

            final_solution.append(current_solution)

        self.solution.set_solutions(final_solution)

    def save_session(self, filename):
        # TODO: Implementar
        pass

    # Metodos para registrar observadores de parametros
    def register_m_observer(self, observer):

        self.m.register(observer)

    def register_solution_observer(self, observer):

        self.solution.register(observer)
