# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from utils.pattern.observer import Subject

"""
Esta clase representa los pares solucion del calculo principal.
"""

class CalculationSolution(Subject):

    def __init__(self):

        super(CalculationSolution, self).__init__()

        # Representa una lista de tuplas (pares solucion)
        self.solution = []

    def set_solution(self, solution):

        self.solution = solution

        # Notifico a observers la nueva solucion para que actualicen
        self.notify_observers(self.solution)

    def get_solution(self):

        return self.solution
