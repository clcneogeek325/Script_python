#!/usr/bin/env python 
import pygtk
pygtk.require('2.0')
import gtk
from Siguente_ventana import ejemlo1

class ejemlo2:
    def __init__(self):
	self.ventana2 = gtk.Window()
	self.ventana2.set_size_request(200,50)
	self.ventana2.set_title("ventana 2")
	self.ventana2.set_position(gtk.WIN_POS_CENTER)

	self.cerrar = gtk.Button("Cerrar")
	self.cerrar.connect("clicked", gtk.main_quit)
	self.cerrar.set_size_request(80,40)
	self.atras = gtk.Button("Atras")
	self.atras.connect("clicked", self.Atras)
	self.atras.set_size_request(80,40)

	self.caja = gtk.HBox()
	self.caja.pack_start(self.cerrar)
	self.caja.pack_start(self.atras)

	self.ventana2.add(self.caja)
	self.ventana2.connect("destroy", gtk.main_quit)
	self.ventana2.show_all()
	

    def Atras(self, widget):
	self.ventana2.destroy()
	app3 = ejemlo2()
	app3.main()


    def main(self):
	gtk.main()

if __name__ == "__main__":
    app = ejemlo2()
    app.main()


