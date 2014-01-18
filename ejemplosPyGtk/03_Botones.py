#!/usr/bin/env python 
import pygtk
pygtk.require('2.0')
import gtk

class ejemlo3:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(300,100)
	self.ventana.set_title("Ejemplo de una etiqueta")
	self.ventana.set_tooltip_text("Dale un click para cerrar la ventana")

        self.boton = gtk.Button("Cerra ventana")
	self.boton.connect("clicked", self.cerrar_ventana)

	self.ventana.add(self.boton)
	self.ventana.connect("destroy", gtk.main_quit)
	self.ventana.show_all()

    def main(self):
	gtk.main()

    def cerrar_ventana(self, widget):
	gtk.main_quit()
	print "La aplicacion ha finalizado"

if __name__ == "__main__":
    app = ejemlo3()
    app.main()


