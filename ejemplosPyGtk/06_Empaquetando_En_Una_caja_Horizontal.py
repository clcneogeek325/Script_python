#!/usr/bin/env python 
import pygtk
pygtk.require('2.0')
import gtk

class ejemlo2:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(500,100)
	self.ventana.set_title("Ejemplo de empaquetado horizontal")
	self.ventana.set_tooltip_text("Esta es una forma de empaquetar elementos en una caja horizontal")

	self.boton = gtk.Button("Boton")

        self.etiqueta = gtk.Label("Empaquetado Horizontal")

	self.entrada_texto = gtk.Entry()

	self.caja = gtk.HBox()

	self.caja.pack_start(self.etiqueta)
	self.caja.pack_start(self.entrada_texto)
	self.caja.pack_start(self.boton)

	self.ventana.add(self.caja)
	self.ventana.connect("destroy", gtk.main_quit)
	self.ventana.show_all()

    def main(self):
	gtk.main()


if __name__ == "__main__":
    app = ejemlo2()
    app.main()


