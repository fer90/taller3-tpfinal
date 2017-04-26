# -*- coding: utf-8 -*-

from view.matplot_figure import MatplotFigure

import numpy as np

"""
Esta clase encapsula todo lo necesario para crear y mostrar plots en la 
interfaz grafica, utilizando la matplotlib
"""

class MatplotCreator(object):

    def __init__(self, plot_view_container, toolbar_view_container):

        self.plot_container = plot_view_container
        self.plot_container_layout = self.plot_container.layout()
        self.toolbar_container = toolbar_view_container
        self.toolbar_container_layout = self.toolbar_container.layout() 

        self.currentPlot = None
        self.there_is_plot = False

    def create_figure(self, solution_list, label = None):
        
        # Este objeto me crea un grafico con los pares solucion de la lista parametro
        figure = MatplotFigure(solution_list, label)

        return figure

    def create_plot(self, figure, need_remove_annotation = True):

        # Elimino el posible widget inicial
        if self.there_is_plot:
            self.remove_plot()
            self.currentPlot = None

        self.currentPlot = figure
        self.add_plot(figure, need_remove_annotation)

    def add_plot(self, figure, need_remove_annotation):

        figure.add_plot(self.toolbar_container, need_remove_annotation)

        self.plot_container_layout.addWidget(self.currentPlot.get_canvas())
        self.toolbar_container_layout.addWidget(self.currentPlot.get_toolbar())

        self.there_is_plot = True

    def remove_plot(self):

        if self.there_is_plot:
            self.plot_container_layout.removeWidget(self.currentPlot.get_canvas())
            self.toolbar_container_layout.removeWidget(self.currentPlot.get_toolbar())
            self.currentPlot.remove_plot()

        self.there_is_plot = False
