# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

"""
Esta clase se encarga genericamente de mostrar dialog boxes
con una entry para llenar
"""
class InputDialogBox(object):

    @staticmethod
    def show_text_input_dialog_box(parent, title, text):

        entry, ok = QInputDialog.getText(parent, title, text)

        if ok:
            return entry
        else:
            return None

    @staticmethod
    def show_item_input_dialog_box(parent, title, text, items):

        entry, ok = QInputDialog.getItem(parent, title, text, items, 0, False)

        if ok:
            return entry
        else:
            return None
