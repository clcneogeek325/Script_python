#!/usr/bin/env python
import pygtk, gtk
pygtk.require('2.0')

class ejemplo1:
    def __init__(self):
        self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.ventana.set_title("Primer ejemplo de pycairo")
        self.ventana.set_position(gtk.WIN_POS_CENTER)
        self.ventana.connect("destroy", self.cerrar)
        self.ventana.show()

    def main(self):
        gtk.main()

    def cerrar(self, widget):
        gtk.main_quit()

objeto = ejemplo1()
objeto.main()
