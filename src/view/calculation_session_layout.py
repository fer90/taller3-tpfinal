# -*- coding: utf-8 -*-

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# Cargo mi diseño de sesion de calculo de solucion
calculation_session_design = uic.loadUiType("designer/calculation_session_layout.ui")[0]

class CalculationSessionLayout(calculation_session_design):

    def __init__(self, identificator):

        super(CalculationSessionLayout, self).__init__()

        self.identificator = identificator

        # Conecto los botones a sus funciones correspondientes
        self.m_calculation_button.clicked.connect(self.m_calculation)

    def m_calculation(self):

        # Obtener todos los parametros de entrada
        """
        TODO: Corroborar que sean ints y no floats
        self.na = self.na_edit_line.text().toInt()
        self.nbr = self.nbr_edit_line.text().toInt()
        self.nc = self.nc_edit_line.text().toInt()
        self.d_nz_from = self.from_parameter_edit_line

        if str(self.d_nz_combo_box.currentText()) == 'Nz':
            self.nbi_min = self.nbi_min_edit_line

        if self.multiple_values_check_box.isChecked():

            self.d_nz_step = self.step_parameter_edit_line
            self.d_nz_to = self.to_parameter_edit_line

        TODO: Crear enum para el modo de ejecucion!
        if self.parallel_mode_button.isChecked():
            self.calculation_mode = Mode.Parallel
        else:
            self.calculation_mode = Mode.Perpendicular
        """

        # Validar parametros de entrada

        # TODO: Llamar al controlador para calcular el valor de m
        # TODO: Utilizar timeout si es necesario
        # A modo de ejemplo, se incluyen solo ciertos valores de m
        self.m_from_value_edit_line.setText("5")
        self.m_to_value_edit_line.setText("20")
