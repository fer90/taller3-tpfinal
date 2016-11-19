# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from model.calculation_session import CalculationSession

class CalculationSessionController(object):

    def __init(self, load_from_file = None):

        super(CalculationSessionController, self).__init__()

        # Crea una instancia de sesion de calculo nueva o carga una por archivo
        self.calculation_session = CalculationSession(load_from_file)

    def solve_m_parameter(self, na, nbr, nc, d, nz, nbi_min, mode):

        self.calculation_session.calcule_m_parameter()

    # Metodos para registrar observadores de parametros
    def register_m_observer(self, observer):

        self.calculation_session.register_m_observer(observer)

    def register_solution_observer(self, observer):

        self.calculation_session.register_solution_observer(observer)
