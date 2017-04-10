# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import logging

import sys
sys.path.append('../')
from utils.pattern.observer import Observer

"""
Esta clase encapsula los objetos de la vista correspondientes a la solucion de los campos.
Por consiguiente, es el Observer del objeto correspondiente en el modelo
"""

class FieldSolutionView(Observer):

    def __init__(self, name, field_view_object):

        super(FieldSolutionView, self).__init__(name)

        self.field_table_view = field_view_object

        self.d_item_column = 0
        self.re_eh_24_item_column = 1
        self.im_eh_24_item_column = 2
        self.re_eh_53_item_column = 3
        self.im_eh_53_item_column = 4

        self.solution_calculated = False

    def notify(self, solution_list):

        # Limpio la tabla de informacion vieja
        self.clear_values()

        # Llega una lista de lista solucion de varios elementos:
        # 1er elemento d', 
        # segundo elemento: lista con dos elementos lista: Parte real e imaginaria de los campos solucion
        # [[d', [[1, 2], [3, 4]]]...[...]]
        for solution in solution_list:
            logging.debug("La solucion particular es: " + str(solution))
            self.add_value(solution, self.field_table_view.rowCount())
            self.solution_calculated = True


    def add_value(self, values_list, row_count):

        d_item = QTableWidgetItem(str(values_list[0]))
        re_eh_24_item = QTableWidgetItem(str(values_list[1][0][0]))
        im_eh_24_item = QTableWidgetItem(str(values_list[1][0][1]))
        re_eh_53_item = QTableWidgetItem(str(values_list[1][1][0]))
        im_eh_53_item = QTableWidgetItem(str(values_list[1][1][1]))

        # Agrego la nueva fila a la tabla
        self.field_table_view.insertRow(row_count)
        self.field_table_view.setItem(row_count, self.d_item_column, d_item)
        self.field_table_view.setItem(row_count, self.re_eh_24_item_column, re_eh_24_item)
        self.field_table_view.setItem(row_count, self.im_eh_24_item_column, im_eh_24_item)
        self.field_table_view.setItem(row_count, self.re_eh_53_item_column, re_eh_53_item)
        self.field_table_view.setItem(row_count, self.im_eh_53_item_column, im_eh_53_item)

    def clear_values(self):

        while (self.field_table_view.rowCount() > 0):
            self.field_table_view.removeRow(0);

        self.solution_calculated = False

    def get_values(self):

        text = ""
        allRows = self.field_table_view.rowCount()
        for row in range(allRows):
            d_item = self.field_table_view.item(row, self.d_item_column).text()
            re_eh_24_item = self.field_table_view.item(row, self.re_eh_24_item_column).text()
            im_eh_24_item = self.field_table_view.item(row, self.im_eh_24_item_column).text()
            re_eh_53_item = self.field_table_view.item(row, self.re_eh_53_item_column).text()
            im_eh_53_item = self.field_table_view.item(row, self.im_eh_53_item_column).text()
            text += d_item + ";" + re_eh_24_item + ";" + im_eh_24_item + ";" + re_eh_53_item + ";" + im_eh_53_item + "\n"

        return text


    def has_solution(self):

        return self.solution_calculated