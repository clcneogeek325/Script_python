#!/usr/bin/env python
import pygtk    # se importan las librerias gtk
pygtk.require('2.0')
import gtk
import os

class Base:
    def destroy(self, widget):
    	print "La ventana ha sido cerrado por un click"
        gtk.main_quit()
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Elementos")
        self.window.set_size_request(500,500)
        self.window.set_border_width(10)
        
        self.imagen = gtk.Image()
        self.imagen.set_from_file("cartel-de-santa-vol-3.jpg")
        
        
        self.caja = gtk.VBox()
        self.caja.pack_start(self.imagen)

        self.window.add(self.caja)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)

    def main(self):
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
