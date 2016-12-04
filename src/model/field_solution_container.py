# -*- coding: utf-8 -*-

from collections import defaultdict

import sys

sys.path.append('../')

from utils.pattern.observer import Subject

"""
Esta clase contiene el valor de los campos calculados de la sesion de campo, 
diferenciadas cada una por el d'/nz al que pertenecen (una sesion puede tener
varios d'/nz para calcular su campo)
"""

class FieldSolutionContainer(Subject):

    def __init__(self):

        super(FieldSolutionContainer, self).__init__()

        # Diccionario con key = d', value = [lista de pares solucion]
        self.values = defaultdict(list)

    def set_solution(self, solution_list):

        # Llega una lista de lista solucion de varios elementos:
        # 1er elemento d', 
        # segundo elemento: lista con dos elementos lista: Parte real e imaginaria de los campos solucion
        # [[d', [[1, 2], [3, 4]]]...[...]]
        for current_solution in solution_list:

            d_key = str(current_solution[0])

            self.values[d_key].append(current_solution[1])

        self.notify_observers(solution_list)
