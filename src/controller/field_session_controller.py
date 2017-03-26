# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from model.calculation_session import CalculationSession
from model.field_session import FieldSession

#from utils.multiple_values_entry_parameter import MultipleValuesEntryParameter

class FieldSessionController(object):

    def __init__(self, load_from_file = None):

        super(FieldSessionController, self).__init__()

        # Crea una instancia de sesion de campo nueva o carga una por archivo
        self.field_session = FieldSession(load_from_file)

    def solve_first_field_parameter(self, calculation_session_name):

        calculation_session = CalculationSession(calculation_session_name)
        # TODO: Agregar parametros correspondientes
        self.field_session.calcule_first_field_magnitude(calculation_session.na, 
            calculation_session.nbr, calculation_session.nc, calculation_session.solution_list, 
            calculation_session.calculation_mode)

    def solve_second_field_parameter(self, calculation_session_name):

        calculation_session = CalculationSession(calculation_session_name)
        # TODO: Agregar parametros correspondientes
        self.field_session.calcule_second_field_magnitude(calculation_session.na, 
            calculation_session.nbr, calculation_session.nc, calculation_session.solution_list, 
            calculation_session.calculation_mode)

    # Metodos para registrar observadores de solucion de campos
    def register_first_field_observer(self, first_observer):

        self.field_session.register_first_field_observer(first_observer)

    def register_second_field_observer(self, second_observer):

        self.field_session.register_second_field_observer(second_observer)
