# -*- coding: utf-8 -*-

import sys
sys.path.append('../')
from utils.pattern.observer import Observer

"""
Esta clase define un objeto de la vista que representa un valos del parametro m
"""

class MParameterView(Observer):

    def __init__(self, name, layout_object):

        super(MParameterView, self).__init__(name)

        self.layout_object = layout_object

    def notify(self, event):

        self.layout_object.setText(str(event))

    def set_value(self, value):

        self.layout_object.setText(str(value))

    def get_value(self):

        # TODO: Validarlo!
        return int(self.layout_object.text())
