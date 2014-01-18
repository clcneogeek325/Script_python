#!/usr/bin/env python

from __future__ import division
from math import pi as M_PI  # used by many snippets
import os.path
import sys

import cairo
import gtk
import pango

width, height = 400, 400

def path_ellipse(ctx, x, y, width, height, angle=0):
    """
    x      - center x
    y      - center y
    width  - width of ellipse  (in x direction when angle=0)
    height - height of ellipse (in y direction when angle=0)
    angle  - angle in radians to rotate, clockwise
    """
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(angle)
    ctx.scale(width / 2.0, height / 2.0)
    ctx.arc(0.0, 0.0, 1.0, 0.0, 2.0 * M_PI)
    ctx.restore()

def expose_event(widget, event):
    ctx = widget.window.cairo_create()
    snippet_normalize(ctx, width, height)
    path_ellipse(ctx, 0.5, 0.5, 1.0, 0.3, M_PI/4.0)

    # fill
    ctx.set_source_rgba(1,0,0,1)
    ctx.fill_preserve()

    # stroke
    # reset identity matrix so line_width is a constant
    # width in device-space, not user-space
    ctx.save()
    ctx.identity_matrix()
    ctx.set_source_rgba(0,0,0,1)
    ctx.set_line_width(3)
    ctx.stroke()
    ctx.restore()

    


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
