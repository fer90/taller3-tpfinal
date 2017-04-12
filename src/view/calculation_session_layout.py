# -*- coding: utf-8 -*-

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import logging, threading, time
import os, sys
sys.path.append('../')

from model.calculation_session import CalculationMode
from controller.calculation_session_controller import CalculationSessionController
from view.calculation_solution_view import CalculationSolutionView
from view.m_parameter_view import MParameterView

from utils.dialog_box import DialogBox
from utils.file_dialog_box import FileDialogBox

# Cargo mi diseño de sesion de calculo de solucion
calculation_session_design = uic.loadUiType("designer/calculation_session_layout.ui")[0]

class CalculationSessionLayout(QWidget, calculation_session_design):

    def __init__(self, calculation_id, filename = None):

        QWidget.__init__(self, None)

        self.setupUi(self)

        self.controller = CalculationSessionController()

        #self.evolution_running = False
        #self.evolution_thread = None
        #self.evolution_thread_cv = threading.Condition()
        #self.keep_evolution_running = False

        if filename is None:
            self.initialize_view_objects()
        else:
            self.initialize_view_objects_from_file(filename)
        self.initialize_view_connections()
        self.initialize_view_observers()

    def initialize_view_objects_from_file(self, filename):

        """
        Formato:
        na;nbr;nc;nbimin
        [d/nz]_from;[d/nz]_step;[d/nz]_to;mode
        d/nz;m_from;m_to
        ...
        [d/nz];x1;y1
        ...
        """

        with open(filename, 'r') as file_handler:

            line = file_handler.readline().rstrip('\n')
            input_parameters = line.split(";")
            self.na = float(input_parameters[0])
            self.nbr = float(input_parameters[1])
            self.nc = float(input_parameters[2])
            if len(input_parameters) == 4:
                self.nbi_min = input_parameters[3]
                self.nz_calculation = True
            else:
                self.nz_calculation = False

            line = file_handler.readline().rstrip('\n')
            d_nz_parameters = line.split(";")
            self.d_nz_from = float(d_nz_parameters[0])
            self.d_nz_step = float(d_nz_parameters[1])
            self.d_nz_to = float(d_nz_parameters[2])
            self.calculation_mode = CalculationMode(int(d_nz_parameters[3]))

            m_values_list = []
            self.m_parameter = MParameterView("m_parameter_table", self.m_value_table)
            for line in file_handler:
                if line == "-----\n":
                    break
                separated_line = line.split(';')
                m_values_list.append([float(separated_line[0]), int(separated_line[1]), int(separated_line[2])])
            if len(m_values_list) > 0:
                self.m_parameter.notify(m_values_list)

            solution_list = []
            self.solution = CalculationSolutionView("solution", self.solution_values_list, self.matplot_container, self.toolbar_container)
            current_d_nz = -1
            current_solution = []

            for line in file_handler:
                logging.debug("La siguiente linea es: " + line)
                separated_line = line.split(';')
                new_d_nz = float(separated_line[0])

                if new_d_nz != current_d_nz:
                    if current_solution:
                        solution_list.append([current_d_nz, [[solution[0] for solution in current_solution], [solution[1] for solution in current_solution]]])
                    current_solution = []
                    current_d_nz = new_d_nz

                current_solution.append([float(separated_line[1]), float(separated_line[2])])

            # Agrego el ultimo d/nz
            if current_solution:
                solution_list.append([current_d_nz, [[solution[0] for solution in current_solution], [solution[1] for solution in current_solution]]])

            if solution_list:
                logging.debug("La lista de soluciones cargadas es: " + str(solution_list))
                self.solution.notify(solution_list)


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
        self.solution = CalculationSolutionView("solution", self.solution_values_list, self.matplot_container, self.toolbar_container)

    def initialize_view_connections(self):

        # Conecto la eleccion de d'/Nz para habilitar/deshabilitar campos
        self.d_nz_combo_box.currentIndexChanged.connect(self.d_nz_change)

        # Conecto eleccion de multiple values para habilitar/deshabilitar campos
        self.multiple_values_check_box.stateChanged.connect(self.multiple_values_state_change)

        # Conecto los botones a sus funciones correspondientes
        self.m_calculation_button.clicked.connect(self.m_calculation)
        self.solution_calculation_button.clicked.connect(self.solution_calculation)
        self.export_calculation_session_button.clicked.connect(self.export_calculation_session)
        #self.evolution_button.clicked.connect(self.manage_evolution)

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
            DialogBox.show_dialog_box(QMessageBox.Critical, "Error en los parametros de entrada", "Error en los parametros de entrada. Revisar que se haya aprovisionado correctamente!")
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

    def save_calculation_session(self, file_handler):

        logging.debug("Se guarda la sesión de cálculo en el archivo " + str(file_handler.name))

        """
        Formato:
        na;nbr;nc;nbimin
        [d/nz]_from;[d/nz]_step;[d/nz]_to;mode
        d/nz;m_from;m_to
        ...
        [d/nz];x1;y1
        ...
        """
        line = ""
        try:
            self.na = float(self.na_edit_line.text())
            self.nbr = float(self.nbr_edit_line.text())
            self.nc = float(self.nc_edit_line.text())

            line = str(self.na) + ";" + str(self.nbr) + ";" + str(self.nc)

            if self.nz_calculation:
                self.nbi_min = float(self.nbi_min_edit_line.text())
                line += ";" + str(self.nbi_min)

            line += "\n"
            file_handler.write(line)
            line = ""

            self.d_nz_from = int(self.from_parameter_edit_line.text())

            line = self.d_nz_from

            if self.multiple_values_check_box.isChecked():

                self.d_nz_step = int(self.step_parameter_edit_line.text())
                self.d_nz_to = int(self.to_parameter_edit_line.text())

            else:

                self.d_nz_step = 1
                self.d_nz_to = self.d_nz_from + 1

            line = str(self.d_nz_from) + ";" + str(self.d_nz_step) + ";" + str(self.d_nz_to) + ";"

            if self.parallel_mode_button.isChecked():
                self.calculation_mode = CalculationMode.Parallel
            else:
                self.calculation_mode = CalculationMode.Perpendicular

            line += str(self.calculation_mode.value) + "\n"
            file_handler.write(line)
            line = ""

            if self.m_parameter.has_solution():
                self.m_parameter.dump_solution(file_handler)
            file_handler.write("-----\n")
            if self.solution.has_solution():
                self.solution.dump_solution(file_handler)
        except ValueError:
            logging.warning("No se ha guardado la sesión por problemas en los parámetros de entrada")
            return False

        return True

    def export_calculation_session(self):

        logging.info("Exportando datos...")

        if self.solution.has_solution():

            # Llamo al pop-up para que el usuario designe el lugar donde se guarda el archivo
            filename = FileDialogBox.show_save_file_dialog_box(self)
            filename += ".txt"

            logging.debug("Saving in file: " + str(filename))
            logging.debug("Opening file '" + str(filename) + "'")

            file_handler = open(filename, 'w')

            try:
                self.solution.dump_solution(file_handler)
            except Exception as e:
                logging.error("Error al exportar datos: " + str(e))
                os.unlink(file_handler.name)
                DialogBox.show_dialog_box(QMessageBox.Critical, "Error exportando datos", "Se ha producido un error al exportar los resultados del cálculo", str(e))
            else:
                file_handler.close()
                logging.info("Datos exportados")
                DialogBox.show_dialog_box(QMessageBox.Information, "Exportar datos", "Se han exportado los resultados satisfactoriamente")

        else:
            logging.debug("No hay datos para exportar")
            DialogBox.show_dialog_box(QMessageBox.Information, "Exportar Datos", "No hay datos para exportar!")

    def stop_session(self):

        # Principalmente, se utiliza para frenar el motor de matlab utilizado
        self.controller.stop_session()

    def manage_evolution(self):

        cant_solutions = self.solution_values_list.count()
        for i in range(cant_solutions):

            self.solution.change_current_figure_on_demand(self.solution_values_list.item(i).text())
            time.sleep(5)

        """
        if self.evolution_running:

            # Freno el thread
            self.keep_evolution_running = False
            del self.evolution_thread
            
            # Cambio nombre a 'Start Evolution'
            self.evolution_button.setText('Start Evolution')

        else:

            # Start thread
            self.keep_evolution_running = True
            self.evolution_thread = threading.Thread(target=self.run_evolution)
            self.evolution_thread.start()

            # Cambio nombre a 'Stop Evolution'
            self.evolution_button.setText('Stop Evolution')
        """

        #self.evolution_running = not self.evolution_running
"""
    def run_evolution(self):

        cant_solutions = self.solution_values_list.count()
        i = 0

        while self.keep_evolution_running:

            self.solution.change_current_figure_on_demand(self.solution_values_list.item(i).text())
            time.sleep(0.75)
            i += 1
            if (i == cant_solutions):
                i = 0
"""