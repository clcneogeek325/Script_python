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
    xc = 0.5
    yc = 0.5
    radius = 0.4
    angle1 = 45.0  * (M_PI/180.0)  #/* angles are specified */
    angle2 = 180.0 * (M_PI/180.0)  #/* in radians           */

    snippet_normalize (ctx, width, height)

    ctx.arc_negative (xc, yc, radius, angle1, angle2)
    ctx.stroke ()

    #/* draw helping lines */
    ctx.set_source_rgba (1,0.2,0.2,0.6)
    ctx.arc (xc, yc, 0.05, 0, 2*M_PI)
    ctx.fill ()
    ctx.set_line_width (0.03)
    ctx.arc (xc, yc, radius, angle1, angle1)
    ctx.line_to (xc, yc)
    ctx.arc (xc, yc, radius, angle2, angle2)
    ctx.line_to (xc, yc)
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
