# -*- coding: utf-8 -*-

from collections import defaultdict

import sys

sys.path.append('../')

from utils.pattern.observer import Subject

"""
Esta clase contiene el valor de todos los rangos 'm' de la sesion, 
diferenciados cada uno por el d' al que pertenecen (una sesion puede 
tener un rango de d')
"""

class MContainer(Subject):

    def __init__(self):

        super(MContainer, self).__init__()

        # Diccionario con key = d', value = (m_from, m_to)
        self.values = defaultdict(set)

    def set_parameters(self, parameters_list):

        # Llega una lista de listas de 3 elementos [[d', m_from, m_to]...]
        for current_parameter in parameters_list:
            d_key = str(current_parameter[0])
            self.values[d_key].add(int(current_parameter[1]))
            self.values[d_key].add(int(current_parameter[2]))

        self.notify_observers(parameters_list)
