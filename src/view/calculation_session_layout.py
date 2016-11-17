# -*- coding: utf-8 -*-

from PyQt4 import uic

# Cargo mi diseño de sesion de calculo de solucion
calculation_session_design = uic.loadUiType("designer/calculation_session_layout.ui")[0]

class CalculationSessionLayout(calculation_session_design):

    def __init__(self, identificator):
        self.identificator = identificator
