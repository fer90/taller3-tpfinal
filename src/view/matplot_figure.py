# -*- coding: utf-8 -*-

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

import sys
sys.path.append('../')
from utils.snap_to_cursor import SnaptoCursor

class MatplotFigure(object):

	def __init__(self, solution_list, label = None):
		self.canvas = None
		self.cursor = None
		self.toolbar = None

		self.figure = Figure()
		self.ax1f1 = self.figure.add_subplot(111)

		self.ax1f1.set_xlabel('Nz')
		self.ax1f1.set_ylabel('Nbi')

		self.x = solution_list[0]
		self.y = solution_list[1]

		self.current_lines = None

		if label is None:
			self.ax1f1.plot(solution_list[0], solution_list[1], "o", solution_list[0], solution_list[1])
			box = self.ax1f1.get_position()
			self.ax1f1.set_position([box.x0, box.y0 * 1.1, box.width, box.height])
		else:
			line1, = self.ax1f1.plot(solution_list[0], solution_list[1], "o")
			line2, = self.ax1f1.plot(solution_list[0], solution_list[1], line1.get_color(), label=label)
			self.current_lines = (line1, line2)
			#self.ax1f1.legend(prop={'size':10})
			# Shrink current axis by 20%
			box = self.ax1f1.get_position()
			self.ax1f1.set_position([box.x0, box.y0, box.width * 0.8, box.height])

			# Put a legend to the right of the current axis
			self.ax1f1.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size':8})

	def get_current_lines(self):

		return self.current_lines

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

		self.cursor.remove_annotation()

		self.canvas.close()

		self.toolbar.close()

		self.cursor = None

	def add_graphics(self, solution_list, label = None):

		line1 = None
		line2 = None
		if label is None:
			self.ax1f1.plot(solution_list[0], solution_list[1], "o", solution_list[0], solution_list[1])
		else:
			line1, = self.ax1f1.plot(solution_list[0], solution_list[1], "o")
			line2, = self.ax1f1.plot(solution_list[0], solution_list[1], line1.get_color(), label=label)
			#self.ax1f1.legend(prop={'size':10})
			# Put a legend to the right of the current axis
			self.ax1f1.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size':8})

		self.cursor.append_x_y(solution_list[0], solution_list[1])

		return (line1, line2)

	def remove_graphics(self, lines):

		lines[0].remove()
		lines[1].remove()

	def remove_points(self, remove_list):

		self.cursor.remove_x_y(remove_list[0], remove_list[1])