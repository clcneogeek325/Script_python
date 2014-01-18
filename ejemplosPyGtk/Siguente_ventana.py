#!/usr/bin/env python 
import pygtk
pygtk.require('2.0')
import gtk
from ventana2 import ejemlo2

class ejemlo1:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(500,500)
	self.ventana.set_title("Ejemplo de la creacion de una ventana")
	self.ventana.set_tooltip_text("Esto es un simple ejemplo de como crear una simple ventana de 500x500 pixeles")

	self.siguiente = gtk.Button("Siguiente")
	self.siguiente.connect("clicked", self.Siguiente)
	self.siguiente.set_size_request(80,40)

	self.caja_fija = gtk.Fixed()
	self.caja_fija.put(self.siguiente,250,100)

	self.ventana.add(self.caja_fija)
	self.ventana.connect("destroy", gtk.main_quit)
	self.ventana.show_all()


    def Siguiente(self, widget):
	self.ventana.destroy()
	app2 = ejemlo2()
	app2.main()

    def main(self):
	gtk.main()

if __name__ == "__main__":
    app = ejemlo1()
    app.main()


