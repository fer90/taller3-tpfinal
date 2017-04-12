# -*- coding: utf-8 -*-

import numpy as np

import logging

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

    def remove_x_y(self, removed_x, removed_y):

        self.x = [x for x in self.x if x not in removed_x]
        self.y = [y for y in self.y if y not in removed_y]

    def remove_annotation(self):

        if self.annotate:
            self.annotate.remove()
            self.canvas.draw()
        if self.txt:
            self.txt.remove()
            self.canvas.draw()

    def mouse_move(self, event):

        if not event.inaxes:
            return

        cursor_x, cursor_y = event.xdata, event.ydata

        if self.x:
            index = np.abs(self.x - cursor_x).argmin()
            if np.abs(self.x[index] - cursor_x) < MIN_DIST and np.abs(self.y[index] - cursor_y) < MIN_DIST:
                data_x = self.x[index]
                data_y = self.y[index]
                if self.annotate:
                    self.annotate.set_position((data_x + SEP, data_y - (SEP * 0.1)))
                    self.annotate.set_text('x=%.18f\ny=%.18f' % (data_x, data_y))
                else:
                    self.create_annotate(data_x, data_y)

                self.txt.set_text('x=%1.18f, y=%1.18f' % (data_x, data_y))
                self.ax.draw_artist(self.annotate)
        else:
            self.annotate.remove()
        self.canvas.draw()