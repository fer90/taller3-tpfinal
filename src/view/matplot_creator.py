# -*- coding: utf-8 -*-

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

import numpy as np

"""
Esta clase encapsula todo lo necesario para crear y mostrar plots en la 
interfaz grafica, utilizando la matplotlib
"""

class MatplotCreator(object):

    def __init__(self, plot_view_container):

        self.plot_container = plot_view_container
        self.plot_container_layout = self.plot_container.layout()

        self.canvas = None
        self.there_is_plot = False

    def create_figure(self, solution_list):

        # Este metodo me crea un grafico con los pares solucion de la lista parametro
        figure = Figure()
        ax1f1 = figure.add_subplot(111)
        ax1f1.plot(np.random.rand(5))

        return figure

    def create_plot(self, figure):

        # Elimino el posible widget inicial
        if self.there_is_plot:
            self.remove_plot()

        self.add_plot(figure)

    def add_plot(self, figure):

        self.canvas = FigureCanvas(figure)
        self.plot_container_layout.addWidget(self.canvas)
        self.canvas.draw()

        self.toolbar = NavigationToolbar(self.canvas, self.plot_container, coordinates=True)
        self.plot_container_layout.addWidget(self.toolbar)

        self.there_is_plot = True

    def remove_plot(self):

        if self.there_is_plot:
            self.plot_container_layout.removeWidget(self.canvas)
            self.canvas.close()
            self.plot_container_layout.removeWidget(self.toolbar)
            self.toolbar.close()
        self.there_is_plot = False
