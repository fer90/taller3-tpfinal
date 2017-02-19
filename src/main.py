#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys
from os import walk
import logging

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic

from view.calculation_session_layout import CalculationSessionLayout
from view.field_session_layout import FieldSessionLayout
from view.comparation_session_layout import ComparationSessionLayout

from utils.dialog_box import DialogBox
from utils.input_dialog_box import InputDialogBox

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
        self.comparation_view = ComparationSessionLayout(self.matplot_container, self.toolbar_container, self.saved_calculation_list, self.saved_calculation_info)

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

        # Obtengo todos los archivos guardados
        files = []
        # TODO: Deshardcodear directorio de sesiones guardadas
        for (dirpath, dirnames, filenames) in walk(os.getcwd() + "/save_sessions/calculation/"):
            files.extend(filenames)
            break
        logging.debug("Los archivos guardados hallados son: " + str(files))
        
        # Muestro un pop-up con una lista de archivos guardados
        session_name = InputDialogBox.show_item_input_dialog_box(self, "Sesiones guardadas", "Elija una de las sesiones guardadas:", files)

        if session_name is not None:

            # Construyo el nombre completo del archivo
            filename = os.getcwd() + "/save_sessions/calculation/" + session_name

            # Obtengo el elegido por el user y agrego un Tab con una nueva session layout
            self.calculation_session_layout = CalculationSessionLayout(self.calculation_id, filename)
            last_index = self.calculation_session_container.addTab(self.calculation_session_layout, session_name)
            self.calculation_session_container.setCurrentIndex(last_index)
            self.calculation_id += 1

    def save_current_calculation_session(self):

        filename = InputDialogBox.show_text_input_dialog_box(self, "Guardar sesión de cálculo", "Ingrese el nombre de la sesión de cálculo: ")

        logging.debug("Se guardará la sesión de cálculo en el archivo: " + str(filename))

        # TODO: Deshardcodear directorio de sesiones guardadas
        file_handler = open(os.getcwd() + "/save_sessions/calculation/" + filename, 'w')
        
        current_session = self.calculation_session_container.currentWidget()

        if current_session.save_calculation_session(file_handler):
            logging.error("Sesión guardada con éxito!")
            # TODO: Modificar titulo del tab!
            file_handler.close()
            DialogBox.show_dialog_box(QMessageBox.Information, "Guardar sesión", "Se ha guardado la sesión satisfactoriamente")
        else:
            logging.error("La sesión no ha podido guardarse!")
            os.unlink(file_handler.name)
            DialogBox.show_dialog_box(QMessageBox.Critical, "Guardar sesión", "No se ha podido guardar la sesión")

    def delete_current_calculation_session(self):

        # TODO: Cartel de ¿Esta seguro?

        # Primero debo frenar la sesion de matlab
        current_session = self.calculation_session_container.currentWidget()
        current_session.stop_session()

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
