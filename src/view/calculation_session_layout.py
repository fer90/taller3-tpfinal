# -*- coding: utf-8 -*-

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys
sys.path.append('../')

from controller.calculation_session_controller import CalculationSessionController

# Cargo mi diseño de sesion de calculo de solucion
calculation_session_design = uic.loadUiType("designer/calculation_session_layout.ui")[0]

class CalculationSessionLayout(QWidget, calculation_session_design):

    def __init__(self, identificator):

        QWidget.__init__(self, None)

        self.setupUi(self)

        self.identificator = identificator
        self.controller = CalculationSessionController()

        # Conecto la eleccion de d'/Nz para habilitar/deshabilitar campos
        self.d_nz_combo_box.currentIndexChanged.connect(self.d_nz_change)

        # Conecto eleccion de multiple values para habilitar/deshabilitar campos
        self.multiple_values_check_box.stateChanged.connect(self.multiple_values_state_change)

        # Conecto los botones a sus funciones correspondientes
        self.m_calculation_button.clicked.connect(self.m_calculation)
        self.solution_calculation_button.clicked.connect(self.solution_calculation)
        self.save_calculation_session_button.clicked.connect(self.save_calculation_session)

    def d_nz_change(self, current_index):

        if str(self.d_nz_combo_box.currentText()) == 'Nz':

            self.nbi_min_label.setEnabled(True)
            self.nbi_min_edit_line.setEnabled(True)

        else:

            self.nbi_min_label.setEnabled(False)
            self.nbi_min_edit_line.setEnabled(False)

    def multiple_values_state_change(self, current_index):

        if self.multiple_values_check_box.isChecked():

            self.step_parameter_edit_line.setEnabled(True)
            self.to_parameter_edit_line.setEnabled(True)

        else:

            self.step_parameter_edit_line.setEnabled(False)
            self.to_parameter_edit_line.setEnabled(False)

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
        # self.controller.solve_m_parameter(self.na, self.nbr, self.nc, self.d_nz_from, self.nz, self.nbi_min, self.calculation_mode)
        self.m_from_value_edit_line.setText("5")
        self.m_to_value_edit_line.setText("20")

    def solution_calculation(self):

        # Obtengo los parametros de 'm' calculados
        """
        self.m_from_value = self.m_from_value_edit_line.text().toInt()
        self.m_to_value = self.m_to_value_edit_line.text().toInt()
        """

        # Validar parametros de entrada

        # TODO: Llamar al controlador, debe llamar al modelo que llama
        # al script en matlab
        # TODO: Se debe devolver un matplot y una lista de valores solución
        self.update_solution_values_list([(1, 2), (2, 2), (3, 4), (4, 5), (10, 10), (4, 6), (1, 12), (50, 12), (12312312312312, 3), (123, 4)])

    def update_solution_values_list(self, solution_values):

        for solution in solution_values:

            self.solution_values_list.addItem(str(solution))

    def save_calculation_session(self):

        # TODO: Llamar al controlador para que guarde la sesion
        pass
