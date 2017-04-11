# -*- coding: utf-8 -*-

import numpy as np

MIN_DIST = 0.05
SEP = 0.01

class SnaptoCursor(object):

    def __init__(self, canvas, ax, x, y):

        self.ax = ax
        self.x = x
        self.y = y
        self.annotate = None
        self.txt = ax.text(0.01, 0.01, '', transform=ax.transAxes)
        self.canvas = canvas

    def create_annotate(self, x, y):

        self.annotate = self.ax.annotate('', size='x-small',
                             xy=(x,y), xytext=(x+SEP, y), 
                             bbox=dict(facecolor='white', boxstyle='round', alpha=0.4))

    def append_x_y(self, x, y):

        self.x = self.x + x
        self.y = self.y + y

    def mouse_move(self, event):

        if not event.inaxes:
            return

        cursor_x, cursor_y = event.xdata, event.ydata
        index = np.abs(self.x - cursor_x).argmin()
        if np.abs(self.x[index] - cursor_x) < MIN_DIST and np.abs(self.y[index] - cursor_y) < MIN_DIST:
            data_x = self.x[index]
            data_y = self.y[index]
            if self.annotate:
                self.annotate.set_position((data_x + SEP, data_y - SEP))
                self.annotate.set_text('x=%.18f\ny=%.18f' % (data_x, data_y))
            else:
                self.create_annotate(data_x, data_y)

            self.txt.set_text('x=%1.18f, y=%1.18f' % (data_x, data_y))
            self.ax.draw_artist(self.annotate)
            self.canvas.draw()