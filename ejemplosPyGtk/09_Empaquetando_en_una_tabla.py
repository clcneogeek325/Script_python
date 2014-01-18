#!/usr/bin/env python
import gtk, pygtk
pygtk.require('2.0')

class tabla:
    def __init__(self):
	self.ventana = gtk.Window( gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position( gtk.WIN_POS_CENTER)
	self.ventana.set_title("Ejemplo de una tabla")
	self.ventana.set_size_request(400,400)
	self.ventana.set_tooltip_text("Esta es la forma de empaquetar pero con una tabla")
	self.table = gtk.Table(3, 3, True)
	self.ventana.add(self.table)

	self.boton1 = gtk.Button("Boton1")
	self.boton2 = gtk.Button("Boton2")
	self.boton3 = gtk.Button("Boton3")
	self.boton4 = gtk.Button("Boton4")
	self.boton5 = gtk.Button("Boton5")
	self.boton6 = gtk.Button("Boton6")
	

	self.table.attach(self.boton1, 0, 1, 0, 1)
	self.table.attach(self.boton2, 1, 3, 0, 1)
	self.table.attach(self.boton3, 0, 1, 1, 3)
	self.table.attach(self.boton4, 1, 3, 1, 2)
	self.table.attach(self.boton5, 1, 2, 2, 3)
	self.table.attach(self.boton6, 2, 3, 2, 3)
	self.ventana.show_all()
	self.ventana.connect("destroy", gtk.main_quit)
tabla()
gtk.main()
