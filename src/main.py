#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import logging

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from view.calculation_session_layout import CalculationSessionLayout
from view.field_session_layout import FieldSessionLayout
from view.comparation_session_layout import ComparationSessionLayout

# Cargo mi diseño de aplicacion principal
main_window = uic.loadUiType("designer/main_application.ui")[0]

class MainWindow(QMainWindow, main_window):

    def __init__(self, parent = None):

        QMainWindow.__init__(self, parent)

        self.setupUi(self)

        # Inicializo IDs de sesion
        # TODO: Levantarlos de disco!
        self.calculation_id = 1
        self.field_id = 1

        # Creo el objeto correspondiente a la pantalla de Comparaciones
        self.comparation_view = ComparationSessionLayout(self.matplot_container, self.saved_calculation_list, self.saved_calculation_info)

        # Le agrego funcionalidad a los botones que abren, cargan y cierran sesiones de calculo y campo
        self.create_new_calculation_button.clicked.connect(self.create_new_calculation_session)
        self.open_saved_calculation_button.clicked.connect(self.open_saved_calculation_session)
        self.delete_calculation_button.clicked.connect(self.delete_current_calculation_session)
        self.save_calculation_button.clicked.connect(self.save_current_calculation_session)

        self.create_field_calculation_button.clicked.connect(self.create_new_field_session)
        self.open_saved_field_calculation.clicked.connect(self.open_saved_field_session)
        self.save_field_calculation_button.clicked.connect(self.save_current_field_session)
        self.delete_field_calculation_button.clicked.connect(self.delete_current_field_session)

    def create_new_calculation_session(self):

        self.calculation_session_layout = CalculationSessionLayout(self.calculation_id)
        last_index = self.calculation_session_container.addTab(self.calculation_session_layout, "NuevaSesionCalculo" + str(self.calculation_id))
        self.calculation_session_container.setCurrentIndex(last_index)

        self.calculation_id += 1

    def open_saved_calculation_session(self):

        pass

    def save_current_calculation_session(self):

        pass

    def delete_current_calculation_session(self):

        # TODO: Cartel de ¿Esta seguro?

        self.calculation_session_container.removeTab(self.calculation_session_container.currentIndex())

    def create_new_field_session(self):

        self.field_session_layout = FieldSessionLayout(self.field_id)
        last_index = self.field_session_container.addTab(self.field_session_layout, "NuevaSesionCampo" + str(self.field_id))
        self.field_session_container.setCurrentIndex(last_index)

        self.field_id += 1

    def open_saved_field_session(self):

        pass

    def save_current_field_session(self):

        pass

    def delete_current_field_session(self):

        # TODO: Cartel de ¿Esta seguro?

        self.field_session_container.removeTab(self.field_session_container.currentIndex())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    logging.basicConfig(level=logging.DEBUG)

    main_window = MainWindow()
    main_window.showMaximized()
    sys.exit(app.exec_())
