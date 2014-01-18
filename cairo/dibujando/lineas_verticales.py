#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import gobject
import gtk, pygtk, cairo
from math import pi


pygtk.require('2.0')

class dibujar:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
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


    def main(self):
	gtk.main()

    def dibujando(self, event, widget):
	ctx = widget.window.cairo_create()
	#fondo del dibujo
        ctx.set_source_rgb(1,1,1 ) # fondo azul
	ctx.rectangle(0, 0, 500, 500)#tamanio del fondo
	ctx.fill()


        ctx.set_source_rgb(0,0,0) # fondo negro
        ctx.set_line_width(20) # tamaño de linea
        ctx.move_to(30,100)
                  # x1   y1 puntos de inicio
        ctx.rel_line_to(0,200)
                       #x2 #y2 apartir del punto x2 
        ctx.stroke()



if __name__ == "__main__":
   objeto = dibujar()
   objeto.main()
