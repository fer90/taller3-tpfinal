# -*- coding: utf-8 -*-

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import logging
import os, sys
sys.path.append('../')

from model.calculation_session import CalculationMode
from controller.calculation_session_controller import CalculationSessionController
from view.calculation_solution_view import CalculationSolutionView
from view.m_parameter_view import MParameterView

# Cargo mi diseño de sesion de calculo de solucion
calculation_session_design = uic.loadUiType("designer/calculation_session_layout.ui")[0]

class CalculationSessionLayout(QWidget, calculation_session_design):

    def __init__(self, identificator):

        QWidget.__init__(self, None)

        self.setupUi(self)

        self.identificator = identificator
        self.controller = CalculationSessionController()

        self.initialize_view_objects()
        self.initialize_view_connections()
        self.initialize_view_observers()

    def initialize_view_objects(self):

        # Parametros iniciales
        self.na = None
        self.nbr = None
        self.nc = None
        self.d_nz_from = None
        self.nbi_min = None
        self.d_nz_step = None
        self.d_nz_to = None
        self.calculation_mode = None

        self.nz_calculation = False

        # Parametro 'm'
        self.m_parameter = MParameterView("m_parameter_table", self.m_value_table)

        # Lista Solucion
        self.solution = CalculationSolutionView("solution", self.solution_values_list, self.matplot_container)

    def initialize_view_connections(self):

        # Conecto la eleccion de d'/Nz para habilitar/deshabilitar campos
        self.d_nz_combo_box.currentIndexChanged.connect(self.d_nz_change)

        # Conecto eleccion de multiple values para habilitar/deshabilitar campos
        self.multiple_values_check_box.stateChanged.connect(self.multiple_values_state_change)

        # Conecto los botones a sus funciones correspondientes
        self.m_calculation_button.clicked.connect(self.m_calculation)
        self.solution_calculation_button.clicked.connect(self.solution_calculation)
        self.export_calculation_session_button.clicked.connect(self.export_calculation_session)

    def initialize_view_observers(self):

        self.controller.register_m_observer(self.m_parameter)
        self.controller.register_solution_observer(self.solution)

    def d_nz_change(self, current_index):

        if str(self.d_nz_combo_box.currentText()) == 'Nz':

            self.nbi_min_label.setEnabled(True)
            self.nbi_min_edit_line.setEnabled(True)

            self.nz_calculation = True

        else:

            self.nbi_min_label.setEnabled(False)
            self.nbi_min_edit_line.setEnabled(False)

            self.nz_calculation = False

    def multiple_values_state_change(self, current_index):

        if self.multiple_values_check_box.isChecked():

            self.step_parameter_edit_line.setEnabled(True)
            self.to_parameter_edit_line.setEnabled(True)

        else:

            self.step_parameter_edit_line.setEnabled(False)
            self.to_parameter_edit_line.setEnabled(False)

    def m_calculation(self):

        # Obtener todos los parametros de entrada
        try:
            self.na = float(self.na_edit_line.text())
            self.nbr = float(self.nbr_edit_line.text())
            self.nc = float(self.nc_edit_line.text())
            self.d_nz_from = int(self.from_parameter_edit_line.text())

            if self.nz_calculation:
                self.nbi_min = float(self.nbi_min_edit_line.text())

            if self.multiple_values_check_box.isChecked():

                self.d_nz_step = int(self.step_parameter_edit_line.text())
                self.d_nz_to = int(self.to_parameter_edit_line.text())

            else:

                self.d_nz_step = 1
                self.d_nz_to = self.d_nz_from + 1

        except ValueError:
            self.show_dialog_box(QMessageBox.Critical, "Error en los parametros de entrada", "Error en los parametros de entrada. Revisar que se haya aprovisionado correctamente!")
            return

        # Checkeo modo de ejecucion
        if self.parallel_mode_button.isChecked():
            self.calculation_mode = CalculationMode.Parallel
        else:
            self.calculation_mode = CalculationMode.Perpendicular

        # Validar parametros de entrada

        self.controller.solve_m_parameter(self.na, self.nbr, self.nc, (self.d_nz_from, self.d_nz_step, self.d_nz_to), self.d_nz_from, self.nbi_min, self.calculation_mode)

    def solution_calculation(self):

        # Obtengo los parametros de d'/Nz y rango de 'm' calculados
        try:
            d_m_values = self.m_parameter.get_values()
        except ValueError:
            # TODO: QDialog avisando que hay parametros incorrectos y retornar
            pass

        # TODO: Validar parametros de entrada

        # Llamo al controlador para ejecutar el calculo
        self.controller.solve_calculation(self.na, self.nbr, self.nc, d_m_values, self.calculation_mode)

    def export_calculation_session(self):

        # TODO: Pop-up para consultar por el nombre del archivo
        filename = QFileDialog.getSaveFileName(self, "Save file", "", ".txt")
        filename += ".txt"

        logging.debug("Saving in file: " + str(filename))
        logging.debug("Opening file '" + str(filename) + "'")

        file_handler = open(filename, 'w')

        try:
            if self.solution.has_solution():
                self.solution.dump_solution(file_handler)
        except Exception as e:
            logging.error("Error al exportar datos: " + str(e))
            os.unlink(file_handler.name)
            self.show_dialog_box(QMessageBox.Critical, "Error exportando datos", "Se ha producido un error al exportar los resultados del cálculo", str(e))
        else:
            file_handler.close()
            self.show_dialog_box(QMessageBox.Information, "Exportar datos", "Se han exportado los resultados satisfactoriamente")

    def show_dialog_box(self, icon, title, text, detailed_text = None, additional_information = None):

        msg = QMessageBox()
        msg.setIcon(icon)

        msg.setText(text)
        if additional_information is not None:
            msg.setInformativeText(additional_information)
        msg.setWindowTitle(title)
        if detailed_text is not None:
            msg.setDetailedText("Detalles: " + detailed_text)
        msg.setStandardButtons(QMessageBox.Ok)
        #msg.buttonClicked.connect(msgbtn)

        retval = msg.exec_()
