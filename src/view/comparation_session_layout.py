# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os, sys
from os import walk
import logging

from view.matplot_creator import MatplotCreator

from model.calculation_session import CalculationSession
from model.calculation_mode import CalculationMode

"""
Esta clase representa la pantalla de Comparaciones
"""

class ComparationSessionLayout(object):

    def __init__(self, matplot_container, toolbar_container, saved_calculations_list_view, saved_calculations_info_view):

        super(ComparationSessionLayout, self).__init__()

        self.matplot_container = matplot_container
        self.toolbar_container = toolbar_container
        self.saved_calculations_list_view = saved_calculations_list_view
        self.saved_calculations_info_view = saved_calculations_info_view

        self.model = None
        layout = QVBoxLayout()
        self.na_widget = QLabel("Na = ")
        layout.addWidget(self.na_widget)
        self.nbr_widget = QLabel("Nbr = ")
        layout.addWidget(self.nbr_widget)
        self.nc_widget = QLabel("Nc = ")
        layout.addWidget(self.nc_widget)
        #self.d_widget = QLabel("d = ")
        self.mode_widget = QLabel("Modo = ")
        layout.addWidget(self.mode_widget)
        self.saved_calculations_info_view.setLayout(layout)

        self.matplot_creator = MatplotCreator(self.matplot_container, self.toolbar_container)
        self.figure = None

        self.calculation_sessions = dict()
        self.lines_index = dict()
        self.legend_index = dict()

        self.initialize_saved_sessions()

    def initialize_saved_sessions(self):

        self.model = QStandardItemModel()

        # Obtengo todos los archivos guardados
        files = []
        # TODO: Deshardcodear directorio de sesiones guardadas
        for (dirpath, dirnames, filenames) in walk(os.getcwd() + "/save_sessions/calculation/"):
            files.extend(filenames)

            break

        for filename in filenames:

            item = QStandardItem(filename)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            item.setData(Qt.Unchecked, Qt.CheckStateRole)
            item.setCheckable(True)
            item.setSelectable(True)
            self.model.appendRow(item)

        self.model.connect(self.model, SIGNAL('itemChanged( QStandardItem *)'), self.item_changed)

        self.saved_calculations_list_view.setModel(self.model)
        self.saved_calculations_list_view.show()

    """
    def selection_item_changed(self, item, anotherItem):

        logging.debug("asdasdasdas")
        calculation_session_name = os.getcwd() + "/save_sessions/calculation/" + item.text()
        calculation_session = CalculationSession(calculation_session_name)
        self.na_widget.setText("Na = " + str(calculation_session.na))
        self.nbr_widget.setText("Nbr = " + str(calculation_session.nbr))
        self.nc_widget.setText("Nc = " + str(calculation_session.nc))
        #self.d_widget.setText("d = " + str(calculation_session.d))
        if calculation_session.calculation_mode == CalculationMode.Parallel:
            self.mode_widget.setText("Modo = PARALELO")
        else:
            self.mode_widget.setText("Modo = PERPENDICULAR")
    """

    def item_changed(self, item):

        if item.checkState() == Qt.Checked:

            calculation_session_name = os.getcwd() + "/save_sessions/calculation/" + item.text()
            calculation_session = CalculationSession(calculation_session_name)

            self.lines_index[item.text()] = list()
            self.legend_index[item.text()] = list()

            for solution in calculation_session.solution_list:
                if self.figure is None:

                    logging.debug("Voy a agregar la solucion " + str(solution))
                    legend = "d' = " + str(solution[0]) + ", Na = " + str(calculation_session.na) + ", \nNbr = " + str(calculation_session.nbr) + ", Nc = " + str(calculation_session.nc)
                    self.figure = self.matplot_creator.create_figure(solution[1], legend)
                    self.matplot_creator.create_plot(self.figure, False)

                    self.lines_index[item.text()].append(self.figure.get_current_lines())
                    self.legend_index[item.text()].append(self.figure.get_current_legend())
                else:

                    logging.debug("Voy a agregar la solucion " + str(solution))
                    legend = "d' = " + str(solution[0]) + ", Na = " + str(calculation_session.na) + ", \nNbr = " + str(calculation_session.nbr) + ", Nc = " + str(calculation_session.nc)
                    line1,line2 = self.figure.add_graphics(solution[1], legend)
                    self.lines_index[item.text()].append((line1, line2))
                    self.legend_index[item.text()].append(legend)

            self.na_widget.setText("Na = " + str(calculation_session.na))
            self.nbr_widget.setText("Nbr = " + str(calculation_session.nbr))
            self.nc_widget.setText("Nc = " + str(calculation_session.nc))
            if calculation_session.calculation_mode == CalculationMode.Parallel:
                self.mode_widget.setText("Modo = PARALELO")
            else:
                self.mode_widget.setText("Modo = PERPENDICULAR")

            self.calculation_sessions[item.text()] = calculation_session

        elif item.checkState() == Qt.Unchecked:

            for solution in self.calculation_sessions[item.text()].solution_list:
                self.figure.remove_points(solution[1])
            for lines in self.lines_index[item.text()]:
                self.figure.remove_graphics(lines)
            #for legend in self.legend_index[item.text()]:
            self.figure.remove_legend()

            del self.lines_index[item.text()]
            del self.calculation_sessions[item.text()]
            del self.legend_index[item.text()]

            # Regenero el legend
            lines_list = list()
            label_list = list()
            for key, value in self.lines_index.items():
                for lines in value:
                    lines_list.append(lines[1])
            for key, value in self.legend_index.items():
                for label in value:
                    label_list.append(label)

            self.figure.add_legend(lines_list, label_list)

    def remove_graphics(self):

        model = self.saved_calculations_list_view.model()

        for index in range(model.rowCount()):

            item = model.item(index)

            if item.checkState() == Qt.Checked:

                for solution in self.calculation_sessions[item.text()].solution_list:
                    self.figure.remove_points(solution[1])
                for lines in self.lines_index[item.text()]:
                    self.figure.remove_graphics(lines)

                del self.lines_index[item.text()]
                del self.calculation_sessions[item.text()]
                del self.legend_index[item.text()]

        if self.figure is not None:
            self.figure.remove_legend()
