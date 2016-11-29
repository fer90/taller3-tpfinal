# -*- coding: utf-8 -*-

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Cargo mi diseño de sesion de calculo de solucion
field_session_design = uic.loadUiType("designer/field_session_layout.ui")[0]

class FieldSessionLayout(QWidget, field_session_design):

    def __init__(self, identificator):

        QWidget.__init__(self, None)

        self.setupUi(self)

        self.identificator = identificator

        # Conecto los botones a sus funciones correspondientes
        self.first_field_calculation_button.clicked.connect(self.first_field_calculation)
        self.second_field_calculation_button.clicked.connect(self.second_field_calculation)
        self.export_field_calculation_button.clicked.connect(self.export_field_session)

    def first_field_calculation(self):

        """
        Primero obtengo el nombre de la sesion de calculo elegida:
        self.first_chosen_calculation = str(self.first_field_combo.currentText())
        """
        # TODO: Llamar al controlador
        # Mock
        self.first_field_eh24_value.setText("1 + 2i")
        self.first_field_eh53_value.setText("4 + 6i")

    def second_field_calculation(self):

        """
        Primero obtengo el nombre de la sesion de calculo elegida:
        self.second_chosen_calculation = str(self.second_field_combo.currentText())
        """
        # TODO: Llamar al controlador
        # Mock
        self.second_field_eh24_value.setText("1 + 2i")
        self.second_field_eh53_value.setText("4 + 6i")

    def export_field_session(self):

        pass
