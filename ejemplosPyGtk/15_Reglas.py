#!/usr/bin/env python 
import pygtk
pygtk.require('2.0')
import gtk

class ejemlo:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(500,500)
	self.ventana.set_title("Ejemplo de Reglas")

	self.tabla = gtk.Table(3,2,gtk.True)
	self.areaDibujo = gtk.DrawingArea()
	self.reglas = gtk.Rule
	

	self.ventana.add(self.tabla)
	self.ventana.connect("destroy", gtk.mainquit)
	self.ventana.show()

    def main(self):
	gtk.main()

if __name__ == "__main__":
    app = ejemlo()
    app.main()


