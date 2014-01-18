#!/usr/bin/env python 
import pygtk
pygtk.require('2.0')
import gtk

class ejemlo1:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(500,500)
	self.ventana.set_title("Ejemplo de la creacion de una ventana")
	self.ventana.set_tooltip_text("Esto es un simple ejemplo de como crear una simple ventana de 500x500 pixeles")
	self.ventana.connect("destroy", gtk.mainquit)
	self.ventana.show()

    def main(self):
	gtk.main()

if __name__ == "__main__":
    app = ejemlo1()
    app.main()


