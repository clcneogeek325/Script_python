#!/usr/bin/env python 
import pygtk
pygtk.require('2.0')
import gtk

class ejemlo2:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(500,500)
	self.ventana.set_title("Ejemplo de empaquetado en un punto fijo")
	self.ventana.set_tooltip_text("Esta es una forma de empaquetar donde\
	los elemnetos esten en un punto fijo y no se muevan")

	self.boton = gtk.Button("Boton")

        self.etiqueta = gtk.Label("Empaquetado Vertical")

	self.entrada_texto = gtk.Entry()

	self.caja_estatica = gtk.Fixed()

	self.caja_estatica.put(self.boton, 50, 50)
	self.caja_estatica.put(self.etiqueta,150, 150)
	self.caja_estatica.put(self.entrada_texto, 300, 300)

	self.ventana.add(self.caja_estatica)
	self.ventana.connect("destroy", gtk.main_quit)
	self.ventana.show_all()

    def main(self):
	gtk.main()


if __name__ == "__main__":
    app = ejemlo2()
    app.main()


