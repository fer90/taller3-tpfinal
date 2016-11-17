# -*- coding: utf-8 -*-

from PyQt4 import uic

# Cargo mi diseño de sesion de calculo de solucion
field_session_design = uic.loadUiType("designer/field_session_layout.ui")[0]

class FieldSessionLayout(field_session_design):

    def __init__(self, identificator):
        self.identificator = identificator
