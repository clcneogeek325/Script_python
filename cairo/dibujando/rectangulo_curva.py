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
    #/* a custom shape, that could be wrapped in a function */
    x0	   = 0.1   #/*< parameters like cairo_rectangle */
    y0	   = 0.1
    rect_width  = 0.8
    rect_height = 0.8
    radius = 0.4   #/*< and an approximate curvature radius */

    snippet_normalize (ctx, width, height)

    x1=x0+rect_width
    y1=y0+rect_height
    #if (!rect_width || !rect_height)
    #    return
    if rect_width/2<radius:
	if rect_height/2<radius:
	    ctx.move_to  (x0, (y0 + y1)/2)
	    ctx.curve_to (x0 ,y0, x0, y0, (x0 + x1)/2, y0)
	    ctx.curve_to (x1, y0, x1, y0, x1, (y0 + y1)/2)
	    ctx.curve_to (x1, y1, x1, y1, (x1 + x0)/2, y1)
	    ctx.curve_to (x0, y1, x0, y1, x0, (y0 + y1)/2)
	else:
	    ctx.move_to  (x0, y0 + radius)
	    ctx.curve_to (x0 ,y0, x0, y0, (x0 + x1)/2, y0)
	    ctx.curve_to (x1, y0, x1, y0, x1, y0 + radius)
	    ctx.line_to (x1 , y1 - radius)
	    ctx.curve_to (x1, y1, x1, y1, (x1 + x0)/2, y1)
	    ctx.curve_to (x0, y1, x0, y1, x0, y1- radius)

    else:
	if rect_height/2<radius:
	    ctx.move_to  (x0, (y0 + y1)/2)
	    ctx.curve_to (x0 , y0, x0 , y0, x0 + radius, y0)
	    ctx.line_to (x1 - radius, y0)
	    ctx.curve_to (x1, y0, x1, y0, x1, (y0 + y1)/2)
	    ctx.curve_to (x1, y1, x1, y1, x1 - radius, y1)
	    ctx.line_to (x0 + radius, y1)
	    ctx.curve_to (x0, y1, x0, y1, x0, (y0 + y1)/2)
	else:
	    ctx.move_to  (x0, y0 + radius)
	    ctx.curve_to (x0 , y0, x0 , y0, x0 + radius, y0)
	    ctx.line_to (x1 - radius, y0)
	    ctx.curve_to (x1, y0, x1, y0, x1, y0 + radius)
	    ctx.line_to (x1 , y1 - radius)
	    ctx.curve_to (x1, y1, x1, y1, x1 - radius, y1)
	    ctx.line_to (x0 + radius, y1)
	    ctx.curve_to (x0, y1, x0, y1, x0, y1- radius)

    ctx.close_path ()

    ctx.set_source_rgb (0.5,0.5,1)
    ctx.fill_preserve ()
    ctx.set_source_rgba (0.5,0,0,0.5)
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
