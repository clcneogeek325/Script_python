#!/usr/bin/env python
import gobject
import gtk, pygtk, cairo
from math import pi


pygtk.require('2.0')

class dibujar:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(520,500)
	self.ventana.set_title("Ejemplo de dibujo")

	self.areaDibujo = gtk.DrawingArea()
	self.areaDibujo.set_size_request(500,500)



	self.ventana.add(self.areaDibujo)
	self.areaDibujo.connect("expose-event", self.dibujando)
	self.ventana.connect("destroy", gtk.main_quit)
	self.ventana.show_all()


    def main(self):
	gtk.main()

    def dibujando(self, event, widget):
	ctx = widget.window.cairo_create()
	ctx.set_operator(cairo.OPERATOR_SOURCE)
        ctx.save()
	pixbuf = gtk.gdk.pixbuf_new_from_file_at_size("20wallpapers-de-mujeres.jpg", 500,500)
	ctx.set_source_pixbuf(pixbuf, 10, 10)
	ctx.paint()
	ctx.restore()


if __name__ == "__main__":
   objeto = dibujar()
   objeto.main()
