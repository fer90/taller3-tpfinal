#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from view.calculation_session_layout import CalculationSessionLayout
from view.field_session_layout import FieldSessionLayout

# Cargo mi diseño de aplicacion principal
main_application = uic.loadUiType("designer/main_application.ui")[0]

class MainWindow(QMainWindow, main_application):

    def __init__(self, parent = None):

        QMainWindow.__init__(self, parent)

        self.setupUi(self)

        # Inicializo IDs de sesion
        # TODO: Levantarlos de disco!
        self.calculation_id = 1
        self.field_id = 1

        # Le agrego funcionalidad a los botones que abren y cierran sesiones de calculo y campo
        self.create_new_calculation_button.clicked.connect(self.create_new_calculation_session)
        self.delete_calculation_button.clicked.connect(self.delete_current_calculation)

        self.create_field_calculation_button.clicked.connect(self.create_new_field_session)
        self.delete_field_calculation_button.clicked.connect(self.delete_current_field_session)

    def create_new_calculation_session(self):

        self.calculation_session = QWidget()
        self.calculation_session_layout = CalculationSessionLayout(self.calculation_id)
        self.calculation_session_layout.setupUi(self.calculation_session)
        self.calculation_session_container.addTab(self.calculation_session, "NuevaSesion" + str(self.calculation_id))

        self.calculation_id += 1

    def delete_current_calculation(self):
        pass

    def create_new_field_session(self):

        self.field_session = QWidget()
        self.field_session_layout = FieldSessionLayout(self.field_id)
        self.field_session_layout.setupUi(self.field_session)
        self.field_session_container.addTab(self.field_session, "NuevaSesion" + str(self.field_id))

        self.field_id += 1

    def delete_current_field_session(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
