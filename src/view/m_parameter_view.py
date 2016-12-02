# -*- coding: utf-8 -*-

from qrangeslider import QRangeSlider

from PyQt4.QtGui import QTableWidgetItem

import sys
sys.path.append('../')
from utils.pattern.observer import Observer

"""
Esta clase define un objeto de la vista que representa un valos del parametro m
Este es una tabla con dos columnas, el d' utilizado y el rango de 'm' en el
que se maneja en base al calculo. El rango esta representado por un 
QRangeSlider: https://github.com/rsgalloway/QRangeSlider
"""

class MParameterView(Observer):

    def __init__(self, name, layout_object):

        super(MParameterView, self).__init__(name)

        self.layout_object = layout_object

        self.d_item_column = 0
        self.m_item_column = 1

    def notify(self, event):

        # Limpio la tabla de informacion vieja
        self.clear_values()

        # El evento de notificacion es una lista de listas de 3 elementos con el orden:
        # (d', m_from, m_to)
        for m_calculation in event:
            self.set_value(m_calculation, self.layout_object.rowCount())

    def set_value(self, values_list, row_count):

        d_item = QTableWidgetItem(str(values_list[0]))
        m_item = QRangeSlider()
        from_value = values_list[1]
        to_value = values_list[2]
        m_item.setMin(max(0, from_value - 10))
        m_item.setMax(to_value + 10)
        m_item.setRange(from_value, to_value)

        # Agrego la nueva fila a la tabla
        self.layout_object.insertRow(row_count)
        self.layout_object.setItem(row_count, self.d_item_column, d_item)
        self.layout_object.setCellWidget(row_count, self.m_item_column, m_item)

    def get_values(self):

        # Devuelve una lista de 3-uplas
        values = []

        row_count = self.layout_object.rowCount()
        for row in range(0, row_count):
            d_item = self.layout_object.item(row, self.d_item_column)
            m_item = self.layout_object.cellWidget(row, self.m_item_column)
            current_value = [float(d_item.text()), m_item.getRange()[0], m_item.getRange()[1]]
            values.append(current_value)

        return values

    def clear_values(self):

        while (self.layout_object.rowCount() > 0):
            self.layout_object.removeRow(0);
