#!/usr/bin/env python
import cairo
import gtk


def expose_event(widget, event):
    ctx = widget.window.cairo_create()
    ctx.set_source_rgb(0.22, 0.08, 0.69) # blue
    ctx.rectangle(0, 0, 400, 150)
    ctx.fill()
     
     # draw text
    ctx.select_font_face('Arial Black')
    ctx.set_font_size(60) # em-square height is 90 pixels
    ctx.move_to(10, 90) # move to point (x, y) = (10, 90)
    ctx.set_source_rgb(1.00, 0.83, 0.00) # yellow
    ctx.show_text('Hello World')
    ctx.stroke() 

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
