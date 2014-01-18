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
    snippet_normalize (ctx, width, height)

    ctx.arc (0.5, 0.5, 0.3, 0, 2 * M_PI)
    ctx.clip ()

    ctx.rectangle (0, 0, 1, 1)
    ctx.fill ()
    ctx.set_source_rgb (0, 1, 0)
    ctx.move_to (0, 0)
    ctx.line_to (1, 1)
    ctx.move_to (1, 0)
    ctx.line_to (0, 1)
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
