#!/usr/bin/env python 
import pygtk
pygtk.require('2.0')
import gtk

class ejemlo2:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(300,100)
	self.ventana.set_title("Ejemplo de una etiqueta")
	self.ventana.set_tooltip_text("Esto es un simple ejemplo de como\
        crear una simple ventana de 500x500 apixeles y aniadirle una etiqueta")

        self.etiqueta = gtk.Label("Soy el famosisimo Hola mundo")
	self.ventana.add(self.etiqueta)
	self.ventana.connect("destroy", gtk.main_quit)
	self.ventana.show_all()

    def main(self):
	gtk.main()

if __name__ == "__main__":
    app = ejemlo2()
    app.main()


