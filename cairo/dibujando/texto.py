#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import cairo
import gtk


def expose_event(widget, event):
    ctx = widget.window.cairo_create()
     
     # dibujando texto
    ctx.select_font_face('Arial Black')#tipo fuente
    ctx.set_font_size(60) # tamaño fuente
    ctx.move_to(10, 90) # punto donde aparerá
    ctx.set_source_rgb(0, 0, 0) # color de texto
    ctx.show_text('Hello World') # el texto
    ctx.stroke() #finalizar el dibujo

win = gtk.Window(gtk.WINDOW_TOPLEVEL)
win.set_position(gtk.WIN_POS_CENTER)
win.set_title("Ejemplo de texto en pygtk")
win.connect('destroy', gtk.main_quit)
drawingarea = gtk.DrawingArea()
win.add(drawingarea)
drawingarea.connect('expose_event', expose_event)
drawingarea.set_size_request(400,150)
win.show_all()
gtk.main()
