# -*- coding: utf-8 -*-

from model.value_container import ValueContainer

"""
Esta clase contiene el valor de todas las soluciones de la sesion, 
diferenciadas cada una por el d' al que pertenecen (una sesion puede 
tener un rango de d')
"""

class SolutionContainer(ValueContainer):

    def __init__(self):

        super(SolutionContainer, self).__init__()

    def set_solutions(self, solution_list):

        print(solution_list)
        # Llega una lista de listas de varios elementos:
        # [[d', [(1, 2), (3, 4), ...]]...[...]]
        for current_solution in solution_list:

            d_key = str(current_solution[0])

            for current_solution_pair in current_solution[1]:

                self.values[d_key].append(current_solution_pair)

        self.notify_observers(solution_list)
