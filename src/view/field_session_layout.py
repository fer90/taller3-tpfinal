# -*- coding: utf-8 -*-

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os, sys
from os import walk

import sys
sys.path.append('../')

from view.field_solution_view import FieldSolutionView
from controller.field_session_controller import FieldSessionController

# Cargo mi diseño de sesion de calculo de campo
field_session_design = uic.loadUiType("designer/field_session_layout.ui")[0]

class FieldSessionLayout(QWidget, field_session_design):

    def __init__(self, identificator):

        QWidget.__init__(self, None)

        self.setupUi(self)

        self.identificator = identificator
        self.controller = FieldSessionController()

        self.initialize_view_objects()
        self.initialize_view_connections()
        self.initialize_view_observers()

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
        calculation_session_name = str(self.first_field_combo.currentText())
        filename = os.getcwd() + "/save_sessions/calculation/" + calculation_session_name

        # Llamo al controlador para resolver el calculo
        self.controller.solve_first_field_parameter(filename)

    def second_field_calculation(self):

        # Primero obtengo el nombre de la sesion de calculo elegida:
        calculation_session_name = str(self.second_field_combo.currentText())
        filename = os.getcwd() + "/save_sessions/calculation/" + calculation_session_name

        # Llamo al controlador para resolver el calculo
        self.controller.solve_second_field_parameter(filename)

    def export_field_session(self):

        pass
