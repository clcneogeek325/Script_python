#!/usr/bin/env python
import gtk, pygtk, cairo
from math import pi
pygtk.require('2.0')

class dibujar:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(300,300)
	self.ventana.set_title("Ejemplo de dibujo")

	self.areaDibujo = gtk.DrawingArea()
	self.areaDibujo.connect("expose-event", self.dibujando)
	self.ventana.add(self.areaDibujo)
	self.ventana.connect("destroy", gtk.main_quit)
	self.ventana.show_all()


    def main(self):
	gtk.main()

    def dibujando(self, event, widget):
	ctx = widget.window.cairo_create()
	#fondo del dibujo
        ctx.set_source_rgb(0.5,0.5,0.5 ) # fondo azul
	ctx.rectangle(0, 0, 300, 300)#tamanio del fondo
	ctx.fill()

	ctx.set_source_rgb(0, 0, 0)
	ctx.rectangle(25, 25, 250,250)
        ctx.fill()

	# draw a rectangle
	ctx.set_source_rgb(1, 1, 1)
	ctx.rectangle(30, 30, 240,240)
        ctx.fill()

	ctx.set_source_rgb(1,0,0)
	ctx.arc(150,150,95,95,365*74)
	ctx.fill()

	ctx.set_source_rgb(1,1,1)
	ctx.arc(150,150,90,90,365*74)
	ctx.fill()

	ctx.set_source_rgb(0,0,.8)
	ctx.rectangle(110,120,5,35)
	ctx.fill()

	ctx.set_source_rgb(0,0,.8)
	ctx.rectangle(180,120,5,35)
	ctx.fill()

	ctx.set_source_rgb(1,0,0)
	ctx.arc(150,150,60,6.8,9)
	ctx.fill()
	
	ctx.set_source_rgb(1,1,1)
	ctx.arc(150,145,60,6.8,9)
	ctx.fill()

if __name__ == "__main__":
   objeto = dibujar()
   objeto.main()