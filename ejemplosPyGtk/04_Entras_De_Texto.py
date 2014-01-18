#!/usr/bin/env python 
import pygtk
pygtk.require('2.0')
import gtk

class ejemlo3:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(300,100)
	self.ventana.set_title("Ejemplo de una entrada de texto")
	self.ventana.set_tooltip_text("Escribe algo")

        self.entrada_texto = gtk.Entry()
	self.entrada_texto.connect("changed", self.al_escribir)

	self.ventana.add(self.entrada_texto)
	self.ventana.connect("destroy", gtk.main_quit)
	self.ventana.show_all()

    def main(self):
	gtk.main()

    def al_escribir(self, widget):
	mensaje = self.entrada_texto.get_text()
	print "Tu has escrito : " + mensaje

if __name__ == "__main__":
    app = ejemlo3()
    app.main()


