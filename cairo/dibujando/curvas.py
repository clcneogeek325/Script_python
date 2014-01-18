#!/usr/bin/env python

from __future__ import division
from math import pi as M_PI  # used by many snippets
import os.path
import sys

import cairo
import gtk
import pango

width, height = 400, 400

def expose_event(widget, event):
    ctx = widget.window.cairo_create()
    x,  y  = 0.1, 0.5
    x1, y1 = 0.4, 0.9
    x2, y2 = 0.6, 0.1
    x3, y3 = 0.9, 0.5

    snippet_normalize (ctx, width, height)

    ctx.move_to (x, y)
    ctx.curve_to (x1, y1, x2, y2, x3, y3)

    ctx.stroke ()

    ctx.set_source_rgba (1,0.2,0.2,0.6)
    ctx.set_line_width (0.03)
    ctx.move_to (x,y);   ctx.line_to (x1,y1)
    ctx.move_to (x2,y2); ctx.line_to (x3,y3)
    ctx.stroke ()

def snippet_normalize (ctx, width, height):
    ctx.scale (width, height)
    ctx.set_line_width (0.04)

win = gtk.Window()
win.connect('destroy', gtk.main_quit)

drawingarea = gtk.DrawingArea()
win.add(drawingarea)
drawingarea.connect('expose_event', expose_event)
drawingarea.set_size_request(600,400)

win.show_all()
gtk.main()
