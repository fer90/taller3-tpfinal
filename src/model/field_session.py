# -*- coding: utf-8 -*-


"""
Esta clase representa el modelo principal de una sesion de la pantalla Campos
"""

class FieldSession(object):

    def __init__(self):

        super(FieldSession, self).__init__()

        if load_file is not None:

            # Cargo el modelo desde un archivo guardado
            pass

        else:

            # Cargo un modelo nuevo
            self.initialize_parameters()

    def initialize_parameters(self):

        self.field_solver = FieldSolver()
