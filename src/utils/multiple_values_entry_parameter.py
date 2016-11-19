# -*- coding: utf-8 -*-

from entry_parameter import EntryParameter

"""
Esta clase define un parametro de entrada de algun tipo de calculo representado
en un rango de valores.
Ademas es un subject que contiene listeners de la GUI que requieren
actualizacion del valor que contienen
"""

class MultipleValuesEntryParameter(EntryParameter):

    def __init__(self, name, value_from = None, value_step = None, value_to = None):

        super(EntryParameter, self).__init__(name, value_from)

        self.value_step = value_step
        self.value_to = value_to

    def set_value_step(self, value_step):

        self.value_step = value_step

    def get_value_step(self):

        return self.value_step

    def set_value_to(self, value_to):

        self.value_to = value_to

        self.notify_observers(self.value_to)

    def get_value_to(self):

        return self.value_to
