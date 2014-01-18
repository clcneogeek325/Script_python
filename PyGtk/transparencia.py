#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
 
import sys
import gtk
import cairo

 
def expose_event(widget, event):
    cr = widget.window.cairo_create()
    size = widget.get_size()
 
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.rectangle(1, 1, size[0]-2, size[1]-2)
 
    cr.set_source_rgba(1, 1, 1, .8)
    cr.stroke_preserve()
 
    cr.set_source_rgba(1, 1, 1, .2)
    cr.fill()

class transparencia():

    win = gtk.Window()
    win.set_size_request(400,250)
    win.set_position(gtk.WIN_POS_MOUSE)
    win.set_decorated(False)
    win.set_app_paintable(True)
    win.set_resizable(False)
        

    win.connect('delete-event', gtk.main_quit)
    win.connect('expose-event', expose_event)
    win.widget_add_events('button-press-event', on_button_press)
    imagen = gtk.Image()
    imagen.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size("Pallazo.png", 350, 200))
    imagen.set_tooltip_text("Una pequeña imagen con fondo transparente")
 
    screen = win.get_screen()
    colormap = screen.get_rgba_colormap()
    win.set_colormap(colormap)
    # avoid flick
    win.realize()
    win.window.set_back_pixmap(None, False)
    win.add(imagen)
    win.show_all()
    gtk.main()
 
 
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
