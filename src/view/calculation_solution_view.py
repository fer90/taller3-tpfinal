# -*- coding: utf-8 -*-

import sys
sys.path.append('../')
from utils.pattern.observer import Observer

"""
Esta clase encapsula los objetos de la vista correspondientes a la solucion.
Por consiguiente, es el Observer del objeto correspondiente en el modelo
"""

class CalculationSolutionView(Observer):

    def __init__(self, name, solution_list_view_object, matplot_view_object):

        super(CalculationSolutionView, self).__init__(name)

        self.solution_list_view = solution_list_view_object
        self.matplot_view = matplot_view_object

    def notify(self, event):

        # El 'evento' es una lista de tuplas a actualizar
        for solution in event:

            self.solution_list_view.addItem(str(solution))
