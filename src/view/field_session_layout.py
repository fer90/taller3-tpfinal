# -*- coding: utf-8 -*-

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os, sys
from os import walk
import logging

import sys
sys.path.append('../')

from view.field_solution_view import FieldSolutionView
from controller.field_session_controller import FieldSessionController

from utils.dialog_box import DialogBox
from utils.file_dialog_box import FileDialogBox

# Cargo mi diseño de sesion de calculo de campo
field_session_design = uic.loadUiType("designer/field_session_layout.ui")[0]

class FieldSessionLayout(QWidget, field_session_design):

    def __init__(self, identificator, filename = None):

        QWidget.__init__(self, None)

        self.setupUi(self)

        self.identificator = identificator
        self.controller = FieldSessionController()

        self.initialize_view_objects()
        if filename is not None:
            self.initialize_view_objects_from_file(filename)
        self.initialize_view_connections()
        self.initialize_view_observers()

    def initialize_view_objects_from_file(self, filename):

        """
        Formato:
        nombreSesionCampo1
        d/nz;Re(EH_2_4);Im(EH_2_4);Re(EH_5_3);Im(EH_5_3)
        ...
        +++++
        nombreSesionCampo2
        d/nz;Re(EH_2_4);Im(EH_2_4);Re(EH_5_3);Im(EH_5_3)
        ...
        """

        with open(filename, 'r') as file_handler:

            line = file_handler.readline().rstrip('\n')

            if line != "+++++":
                # Tengo el primer calculo de campo
                self.first_calculation_session_name = line
                current_d = None
                d_values_list = list()
                field_values_list = list()
                for line in file_handler:
                    if line == "-----\n" or line == "+++++\n":
                        break
                    separated_line = line.split(';')

                    field_values_list.append([separated_line[0], [[separated_line[1], separated_line[2]], [separated_line[3], separated_line[4]]]])

                if len(field_values_list) > 0:
                    self.first_field_solution_view.notify(field_values_list)

                if line == "+++++\n":

                    line = file_handler.readline().rstrip('\n')
                    self.second_calculation_session_name = line
                    current_d = None
                    d_values_list = list()
                    field_values_list = list()
                    for line in file_handler:
                        if line == "-----\n" or line == "+++++\n":
                            break
                        line = line.rstrip('\n')
                        logging.debug(str(line))
                        separated_line = line.split(';')

                        field_values_list.append([separated_line[0], [[separated_line[1], separated_line[2]], [separated_line[3], separated_line[4]]]])

                if len(field_values_list) > 0:
                    logging.debug("La lista de valores cargados es: " + str(field_values_list))
                    self.second_field_solution_view.notify(field_values_list)

    def initialize_view_objects(self):

        # Inicializo los combos con los nombres de las sesiones de calculo guardadas
        # 1) Obtengo todos los archivos guardados
        files = []
        # TODO: Deshardcodear directorio de sesiones guardadas
        for (dirpath, dirnames, filenames) in walk(os.getcwd() + "/save_sessions/calculation/"):

            self.first_field_combo.clear()
            self.first_field_combo.addItems(filenames)
            self.second_field_combo.clear()
            self.second_field_combo.addItems(filenames)

            break

        # Inicializo las tablas solucion
        self.first_field_solution_view = FieldSolutionView("First Field Solution View", self.first_field_solution_table)
        self.second_field_solution_view = FieldSolutionView("Second Field Solution View", self.second_field_solution_table)

        self.first_calculation_session_name = None
        self.second_calculation_session_name = None

    def initialize_view_connections(self):

        # Conecto los botones a sus funciones correspondientes
        self.first_field_calculation_button.clicked.connect(self.first_field_calculation)
        self.second_field_calculation_button.clicked.connect(self.second_field_calculation)
        self.export_field_calculation_button.clicked.connect(self.export_field_session)

    def initialize_view_observers(self):

        self.controller.register_first_field_observer(self.first_field_solution_view)
        self.controller.register_second_field_observer(self.second_field_solution_view)

    def first_field_calculation(self):

        # Primero obtengo el nombre de la sesion de calculo elegida
        self.first_calculation_session_name = str(self.first_field_combo.currentText())
        filename = os.getcwd() + "/save_sessions/calculation/" + self.first_calculation_session_name

        # Llamo al controlador para resolver el calculo
        self.controller.solve_first_field_parameter(filename)

    def second_field_calculation(self):

        # Primero obtengo el nombre de la sesion de calculo elegida:
        self.second_calculation_session_name = str(self.second_field_combo.currentText())
        filename = os.getcwd() + "/save_sessions/calculation/" + self.second_calculation_session_name

        # Llamo al controlador para resolver el calculo
        self.controller.solve_second_field_parameter(filename)

    def save_field_session(self, file_handler):

        logging.debug("Se guarda la sesión de campo en el archivo " + str(file_handler.name))

        """
        Formato:
        nombreSesionCalculo1
        d/nz;Re(EH_2_4);Im(EH_2_4);Re(EH_5_3);Im(EH_5_3)
        ...
        +++++
        nombreSesionCalculo2
        d/nz;Re(EH_2_4);Im(EH_2_4);Re(EH_5_3);Im(EH_5_3)
        ...
        """
        line = ""
        try:

            if self.first_calculation_session_name is not None:
                line = str(self.first_calculation_session_name)

            line += "\n"
            file_handler.write(line)
            line = ""

            # Iterar sobre todos los valores de la tabla1
            file_handler.write(self.first_field_solution_view.get_values())

            if self.second_calculation_session_name is not None:
                line = "+++++\n" + str(self.second_calculation_session_name) + "\n"
                file_handler.write(line)
                file_handler.write(self.second_field_solution_view.get_values())
            else:
                line = "-----\n"
                file_handler.write(line)

        except ValueError:
            logging.warning("No se ha guardado la sesión por problemas en los parámetros de entrada")
            return False

        return True

    def export_field_session(self):

        logging.info("Exportando datos de campo...")

        if self.first_field_solution_view.has_solution() or self.second_field_solution_view.has_solution():

            # Llamo al pop-up para que el usuario designe el lugar donde se guarda el archivo
            filename = FileDialogBox.show_save_file_dialog_box(self)
            filename += ".txt"

            logging.debug("Saving in file: " + str(filename))
            logging.debug("Opening file '" + str(filename) + "'")

            file_handler = open(filename, 'w')

            try:

                if self.first_field_solution_view.has_solution():
                    file_handler.write(self.first_calculation_session_name + "\n")
                    file_handler.write(self.first_field_solution_view.get_values())
                if self.second_field_solution_view.has_solution():
                    file_handler.write("-----\n")
                    file_handler.write(self.second_calculation_session_name + "\n")
                    file_handler.write(self.second_field_solution_view.get_values())

            except Exception as e:

                logging.error("Error al exportar datos: " + str(e))
                os.unlink(file_handler.name)
                DialogBox.show_dialog_box(QMessageBox.Critical, "Error exportando datos", "Se ha producido un error al exportar los resultados del campo", str(e))

            else:

                file_handler.close()
                logging.info("Datos exportados")
                DialogBox.show_dialog_box(QMessageBox.Information, "Exportar datos", "Se han exportado los resultados satisfactoriamente")

        else:
            logging.debug("No hay datos para exportar")
            DialogBox.show_dialog_box(QMessageBox.Information, "Exportar Datos", "No hay datos para exportar!")
