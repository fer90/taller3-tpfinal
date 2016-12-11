# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

"""
Esta clase se encarga genericamente de mostrar dialog boxes
con el texto correspondiente
"""
class DialogBox(object):

    @staticmethod
    def show_dialog_box(icon, title, text, detailed_text = None, additional_information = None):

        msg = QMessageBox()
        msg.setIcon(icon)

        msg.setText(text)
        if additional_information is not None:
            msg.setInformativeText(additional_information)
        msg.setWindowTitle(title)
        if detailed_text is not None:
            msg.setDetailedText("Detalles: " + detailed_text)
        msg.setStandardButtons(QMessageBox.Ok)

        retval = msg.exec_()
