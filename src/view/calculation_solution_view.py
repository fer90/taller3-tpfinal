# -*- coding: utf-8 -*-

import logging
import sys
sys.path.append('../')
from utils.pattern.observer import Observer

from view.matplot_creator import MatplotCreator
"""
Esta clase encapsula los objetos de la vista correspondientes a la solucion.
Por consiguiente, es el Observer del objeto correspondiente en el modelo
"""

class CalculationSolutionView(Observer):

    def __init__(self, name, solution_list_view_object, matplot_view_object, matplot_toolbar_view_object):

        super(CalculationSolutionView, self).__init__(name)

        self.solution_list_view = solution_list_view_object
        self.matplot_view = matplot_view_object
        self.matplot_toolbar_view = matplot_toolbar_view_object

        self.matplot_creator = MatplotCreator(self.matplot_view, self.matplot_toolbar_view)

        self.figure_list = dict()

        self.solution_list_view.itemClicked.connect(self.change_current_figure)

        self.solution_list = None

    def notify(self, solution_list):

        # TODO: Refactorizar para permitir el Update de 1 solo grafico (y no borrar y crear todo de vuelta)
        self.figure_list = dict()
        self.solution_list_view.clear()
        self.matplot_creator.remove_plot()

        self.solution_list = solution_list

        # Me notifican una lista de soluciones
        # En cada solucion tengo el d' como primer elemento y una lista con 
        # los pares solucion como segundo elemento
        for solution in solution_list:

            name = "d'/Nz = " + str(solution[0])
            self.figure_list[name] = self.matplot_creator.create_figure(solution[1])
            self.solution_list_view.addItem(name)

        self.solution_list_view.setCurrentRow(0)

    def change_current_figure(self, item_selected):

        text = item_selected.text()
        self.matplot_creator.create_plot(self.figure_list[text])

    def has_solution(self):

        return self.solution_list is not None

    def dump_solution(self, file_handler):

        logging.info("Dumpeando solución...")
        logging.debug("La solucion a dumpear es: " + str(self.solution_list))

        # Imprimo linea a linea en formato d'; nz; nbi
        for solution_d in self.solution_list:
            for i in range(len(solution_d[1][0])):

                line = str(solution_d[0]) + ";"
                line += str(solution_d[1][0][i]) + ";" + str(solution_d[1][1][i]) + "\n"

                logging.debug("Printing: '" + line + "'")

                file_handler.write(line)
