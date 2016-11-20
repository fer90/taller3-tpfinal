# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from model.calculation_session import CalculationSession

class CalculationSessionController(object):

    def __init__(self, load_from_file = None):

        super(CalculationSessionController, self).__init__()

        # Crea una instancia de sesion de calculo nueva o carga una por archivo
        self.calculation_session = CalculationSession(load_from_file)

    def solve_m_parameter(self, na, nbr, nc, d, nz, nbi_min, mode):

        self.calculation_session.calcule_m_parameter(na, nbr, nc, d, nz, nbi_min, mode)

    # Los parametros de 'm' pudieron haber sido cambiados manualmente 
    # por el usuario, por eso se los pasa nuevamente
    def solve_calculation(self, m_from, m_to):

      self.calculation_session.calcule_solution(m_from, m_to)  

    # Metodos para registrar observadores de parametros
    def register_m_observers(self, from_observer, to_observer):

        self.calculation_session.register_m_from_observer(from_observer)
        self.calculation_session.register_m_to_observer(to_observer)

    def register_solution_observer(self, observer):

        self.calculation_session.register_solution_observer(observer)
