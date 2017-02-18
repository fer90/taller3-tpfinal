# -*- coding: utf-8 -*-

from model.value_container import ValueContainer

"""
Esta clase contiene el valor de todos los rangos 'm' de la sesion, 
diferenciados cada uno por el d' al que pertenecen (una sesion puede 
tener un rango de d')
"""

class MContainer(ValueContainer):

    def __init__(self):

        super(MContainer, self).__init__()

    def set_solutions(self, solution_list):

        # Llega una lista de listas de 3 elementos [[d', m_from, m_to]...]
        for current_solution in solution_list:
            d_key = str(current_solution[0])
            self.values[d_key].append(int(current_solution[1]))
            self.values[d_key].append(int(current_solution[2]))

        self.notify_observers(solution_list)
