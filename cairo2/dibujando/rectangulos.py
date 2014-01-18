#!/usr/bin/env python
import gtk, pygtk, cairo
import math


pygtk.require('2.0')

class dibujar:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position( gtk.WIN_POS_CENTER_ALWAYS)
	self.ventana.set_size_request(500,500)
	self.ventana.set_title("Ejemplo de dibujo")

	self.areaDibujo = gtk.DrawingArea()
	self.areaDibujo.set_size_request(500,500)

	self.caja = gtk.VBox()
	self.caja.pack_start(self.areaDibujo)


	self.ventana.add(self.caja)
	self.areaDibujo.connect("expose-event", self.dibujando)
	self.ventana.connect("destroy", gtk.main_quit)
	self.ventana.show_all()
	self.ventana.set_resizable(False)


    def main(self):
	gtk.main()

    def dibujando(self, event, widget):
	ctx = widget.window.cairo_create()
        #poniendole un fondo blanco de 500x500 pixeles
        #ctx.arc( x , y , radio ,angulo 1, angulo 2)
	ctx.set_source_rgb(1, 1, 1)
	ctx.rectangle(0,0, 500,500)
        ctx.fill()

	ctx.set_source_rgb(0, 1, 0)
	ctx.rectangle(100,200, 250,150)
        ctx.fill()
	


if __name__ == "__main__":
   objeto = dibujar()
   objeto.main()
