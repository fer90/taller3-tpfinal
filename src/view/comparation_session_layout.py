# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from view.matplot_creator import MatplotCreator

"""
Esta clase representa la pantalla de Comparaciones
"""

class ComparationSessionLayout(object):

    def __init__(self, matplot_container, saved_calculations_list_view, saved_calculations_info_view):

        super(ComparationSessionLayout, self).__init__()

        self.matplot_containter = matplot_container
        self.saved_calculations_list_view = saved_calculations_list_view
        self.saved_calculations_info_view = saved_calculations_info_view

        self.matplot_creator = MatplotCreator(self.matplot_containter)

        self.initialize_saved_sessions()

    def initialize_saved_sessions(self):

        # TODO: Cargar los nombres de calculos guardados y agregarlos a la lista
        model = QStandardItemModel()

        item = QStandardItem("Primer Calculo Guardado (d' = 20)")
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        item.setCheckable(True)
        item.setSelectable(True)
        model.appendRow(item)
        model.connect(model, SIGNAL('itemChanged( QStandardItem *)'), self.item_changed)
        item = QStandardItem("Segundo Calculo Guardado (Nz = 12)")
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        item.setCheckable(True)
        item.setSelectable(True)
        model.appendRow(item)
        item = QStandardItem("Tercer Calculo Guardado (d' = 300)")
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        item.setCheckable(True)
        item.setSelectable(True)
        model.appendRow(item)

        self.saved_calculations_list_view.setModel(model)
        self.saved_calculations_list_view.show()

    def item_changed(self):

        self.matplot_creator.create_plot([])

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Na = 1"))
        layout.addWidget(QLabel("Nbr = 1.5"))
        layout.addWidget(QLabel("Nc = 1"))
        layout.addWidget(QLabel("d' = 10"))
        layout.addWidget(QLabel("Modo Paralelo"))
        self.saved_calculations_info_view.setLayout(layout)
