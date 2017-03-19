# -*- coding: utf-8 -*-

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

import sys
sys.path.append('../')
from utils.snap_to_cursor import SnaptoCursor

class MatplotFigure(object):

	def __init__(self, solution_list):

		self.canvas = None
		self.cursor = None
		self.toolbar = None

		self.figure = Figure()
		self.ax1f1 = self.figure.add_subplot(111)

		self.x = solution_list[0]
		self.y = solution_list[1]
		self.ax1f1.plot(solution_list[0], solution_list[1], "ob", solution_list[0], solution_list[1])

	def get_canvas(self):

		return self.canvas

	def get_toolbar(self):

		return self.toolbar

	def add_plot(self, toolbar_container):

		self.canvas = FigureCanvas(self.figure)

		# Creo el cursor que se mostrara en el grafico. Le paso el canvas y la lista de puntos
		self.cursor = SnaptoCursor(self.canvas, self.ax1f1, self.x, self.y)

		# El evento de movimiento de cursor se conecta al plot
		self.canvas.mpl_connect('motion_notify_event', self.cursor.mouse_move)

		self.canvas.draw()

		self.toolbar = NavigationToolbar(self.canvas, toolbar_container, coordinates=True)

	def remove_plot(self):

		self.canvas.close()

		self.toolbar.close()

		self.cursor = None