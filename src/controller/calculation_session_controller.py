# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from model.calculation_session import CalculationSession

from utils.multiple_values_entry_parameter import MultipleValuesEntryParameter

class CalculationSessionController(object):

    def __init__(self, load_from_file = None):

        super(CalculationSessionController, self).__init__()

        # Crea una instancia de sesion de calculo nueva o carga una por archivo
        self.calculation_session = CalculationSession(load_from_file)

    def solve_m_parameter(self, na, nbr, nc, d, nz, nbi_min, mode):

        # TODO: Hacerlo mas limpio
        d_range = MultipleValuesEntryParameter("d'", d[0], d[1], d[2])
        self.calculation_session.calcule_m_parameter(na, nbr, nc, d_range, nz, nbi_min, mode)

    # Los parametros de 'm' pudieron haber sido cambiados manualmente 
    # por el usuario, por eso se los pasa nuevamente
    def solve_calculation(self, na, nbr, nc, d_m_values):

      self.calculation_session.calcule_solution(na, nbr, nc, d_m_values)

    # Metodos para registrar observadores de parametros
    def register_m_observer(self, m_observer):

        self.calculation_session.register_m_observer(m_observer)

    def register_solution_observer(self, observer):

        self.calculation_session.register_solution_observer(observer)
