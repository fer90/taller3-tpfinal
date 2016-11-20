# -*- coding: utf-8 -*-

from utils.entry_parameter import EntryParameter

"""
Esta clase define un parametro de entrada de algun tipo de calculo representado
en un rango de valores.
Ademas es un subject que contiene listeners de la GUI que requieren
actualizacion del valor que contienen
"""

class MultipleValuesEntryParameter(object):

    def __init__(self, name, value_from = None, value_step = None, value_to = None):

        super(MultipleValuesEntryParameter, self).__init__()

        self.name = name

        self.value_from = EntryParameter(name + "_from", value_from)
        self.value_step = EntryParameter(name + "_step", value_step)
        self.value_to = EntryParameter(name + "_to", value_to)

    def set_value_from(self, value_from):

        self.value_from.set_value(value_from)

    def get_value_from(self):

        return self.value_from.get_value()

    def set_value_step(self, value_step):

        self.value_step.set_value(value_step)

    def get_value_step(self):

        return self.value_step.get_value()

    def set_value_to(self, value_to):

        self.value_to.set_value(value_to)

    def get_value_to(self):

        return self.value_to.get_value()

    # Metodos para registrar observadores de cada valor
    def register_from_observer(self, observer):

        self.value_from.register(observer)

    def register_step_observer(self, observer):

        self.value_step.register(observer)

    def register_to_observer(self, observer):

        self.value_to.register(observer)
