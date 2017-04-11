# -*- coding: utf-8 -*-

from utils.pattern.observer import Subject

"""
Esta clase define un parametro de entrada de algun tipo de calculo
Ademas es un subject que contiene listeners de la GUI que requieren
actualizacion del valor que contienen
"""

class EntryParameter(Subject):

    def __init__(self, name, value = None):

        super(EntryParameter, self).__init__()

        self.name = name
        self.value = value

    def set_value(self, value):

        self.value = value

        self.notify_observers(self.value)

    def get_value(self):

        return self.value

    def __str__(self):

    	return str(self.value)