# -*- coding: utf-8 -*-

import os, logging

from PyQt4.QtCore import *
from PyQt4.QtGui import *

"""
Esta clase se encarga genericamente de mostrar file dialog boxes
para cargar/guardar archivo
"""
class FileDialogBox(object):

    current_dir = ""
    file_dialog = None

    @staticmethod
    def show_save_file_dialog_box(parent):

        return QFileDialog.getSaveFileName(parent, "Save file", "", ".txt")

    @staticmethod
    def show_save_session_file_dialog_box(parent, fixed_dir = True, calculation = True):

        inner_dir = ""
        if calculation:
            inner_dir = "calculation"
        else:
            inner_dir = "field"

        FileDialogBox.current_dir = os.getcwd() + "/save_sessions/" + inner_dir

        FileDialogBox.file_dialog = QFileDialog()
        if fixed_dir:
            FileDialogBox.file_dialog.directoryEntered.connect(FileDialogBox.set_current_dir)

        return FileDialogBox.file_dialog.getSaveFileName(parent, "Save file", FileDialogBox.current_dir, ".txt")

    @staticmethod
    def set_current_dir():

        logging.debug("Cambio de directorio capturado")
        FileDialogBox.setDirectory(FileDialogBox.current_dir)
