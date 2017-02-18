# -*- coding: utf-8 -*-

from collections import defaultdict

import sys
import abc

sys.path.append('../')

from utils.pattern.observer import Subject

"""
Esta clase contiene en un diccionario una lista de valores
Esta lista se maneja polinomicamente en cada clase hija, por 
lo que puede estar estructura de cualquier forma
"""

class ValueContainer(Subject):
    __metaclass__  = abc.ABCMeta

    def __init__(self):

        super(ValueContainer, self).__init__()

        # Diccionario con key = d', value = [lista particular]
        self.values = defaultdict(list)

    @abc.abstractmethod
    def set_solutions(self, solution_list):
        """
        Cada lista solucion es particular del contenedor
        Debe implementarse en cada clase hija
        """
