# -*- coding: utf-8 -*-

from model.field_solver import FieldSolver
from model.field_solution_container import FieldSolutionContainer
#from utils.entry_parameter import EntryParameter
#from utils.multiple_values_entry_parameter import MultipleValuesEntryParameter

"""
Esta clase representa el modelo de una sesion de pantalla 'campos'.
Se encarga de mantener los datos de una sesion, como asi tambien de ejecutar 
el calculo de la solucion para la magnitud de los campos de las sesiones de 
calculo elegidas
"""

class FieldSession(object):

    def __init__(self, load_file = None):

        if load_file is not None:

            # Cargo el modelo desde un archivo guardado
            pass

        else:

            # Cargo un modelo nuevo
            self.initialize_parameters()

    def initialize_parameters(self):

        # Parametros de entrada iniciales
        self.first_field_solution = FieldSolutionContainer()
        self.second_field_solution = FieldSolutionContainer()

        # Resolvedor de todos los calculos (ifaz hacia matlab de ser necesario)
        self.field_solver = FieldSolver()

    # Param 'solution': Contiene una lista de la forma [[d1, [nz, nbi]]...]
    def calcule_field_magnitude(self, na, nbr, nc, solution, mode):

        field_solution = []

        for elem in solution:

            for points in elem[1]:

                current_solution = []

                current_solution.append(elem[0])

                current_field_solution = self.field_solver.solve_field(na, nbr, points[1], nc, points[0], elem[0], mode)

                current_solution.append(current_field_solution)

                field_solution.append(current_solution)

        return field_solution

    # TODO: Agregar parametros
    def calcule_first_field_magnitude(self, na, nbr, nc, solution, mode):

        self.first_field_solution.set_solution(self.calcule_field_magnitude(na, nbr, nc, solution, mode))

    # TODO: Agregar parametros
    def calcule_second_field_magnitude(self, na, nbr, nc, solution, mode):

        self.second_field_solution.set_solution(self.calcule_field_magnitude(na, nbr, nc, solution, mode))

    def save_session(self, filename):
        # TODO: Implementar
        pass

    # Metodos para registrar observadores de parametros
    def register_first_field_observer(self, observer):

        self.first_field_solution.register(observer)

    def register_second_field_observer(self, observer):

        self.second_field_solution.register(observer)
