# -*- coding: utf-8 -*-

import sys
import logging

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

        """
        Formato:
        na;nbr;nc;nbimin
        [d/nz]_from;[d/nz]_step;[d/nz]_to;mode
        d/nz;m_from;m_to
        ...
        [d/nz];x1;y1
        ...
        """

        with open(filename, 'r') as file_handler:

            line = file_handler.readline().rstrip('\n')
            input_parameters = line.split(";")
            self.na = float(input_parameters[0])
            self.nbr = float(input_parameters[1])
            self.nc = float(input_parameters[2])
            if len(input_parameters) == 4:
                self.nbi_min = input_parameters[3]

            line = file_handler.readline().rstrip('\n')
            d_nz_parameters = line.split(";")
            self.d_nz_from = float(d_nz_parameters[0])
            self.d_nz_step = float(d_nz_parameters[1])
            self.d_nz_to = float(d_nz_parameters[2])
            self.calculation_mode = CalculationMode(int(d_nz_parameters[3]))

            m_values_list = []
            #self.m_parameter = MParameterView("m_parameter_table", self.m_value_table)
            for line in file_handler:
                if line == "-----\n":
                    break
                separated_line = line.split(';')
                m_values_list.append([float(separated_line[0]), int(separated_line[1]), int(separated_line[2])])
            if len(m_values_list) > 0:
                pass
                #self.m_parameter.notify(m_values_list)

            self.solution_list = []
            #self.solution = CalculationSolutionView("solution", self.solution_values_list, self.matplot_container, self.toolbar_container)
            current_d_nz = -1
            current_solution = []

            for line in file_handler:
                logging.debug("La siguiente linea es: " + line)
                separated_line = line.split(';')
                new_d_nz = float(separated_line[0])

                if new_d_nz != current_d_nz:
                    if current_solution:
                        self.solution_list.append([current_d_nz, [[solution[0] for solution in current_solution], [solution[1] for solution in current_solution]]])
                    current_solution = []
                    current_d_nz = new_d_nz

                current_solution.append([float(separated_line[1]), float(separated_line[2])])

            # Agrego el ultimo d/nz
            if current_solution:
                self.solution_list.append([current_d_nz, [[solution[0] for solution in current_solution], [solution[1] for solution in current_solution]]])

            if self.solution_list:
                logging.debug("La lista de soluciones cargadas es: " + str(self.solution_list))
                #self.solution.notify(self.solution_list)
        #self.d = MultipleValuesEntryParameter("d'", 2, 2, 10)

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
        self.solution_list = None

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

        self.m.set_solutions(m_solution)

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

    def stop_session(self):

        self.calculation_solver.stop()