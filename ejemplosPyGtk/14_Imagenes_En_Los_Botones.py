#!/usr/bin/env python
from gi.repository import Gtk
#import Gtk, pyGtk
#pyGtk.require('2.0')

class tabla:
    def __init__(self):
	self.ventana = Gtk.Window( )
	#self.ventana.set_position( Gtk.WIN_POS_CENTER)
	self.ventana.set_title("Ejemplo de botones de Activacion")
	self.ventana.set_size_request(400,400)
	self.ventana.set_tooltip_text("Ejemplo sobloe botones activables")

	self.boton1 = Gtk.Button()
	self.imagen1 = Gtk.Image()
	self.imagen1.set_from_file("evince.png")
	self.boton1.set_border_width(15)
	self.boton1.add(self.imagen1)
	self.boton1.set_tooltip_text("Este es el boton 1")
	self.boton2 = Gtk.Button()
	self.imagen2 = Gtk.Image()
	self.imagen2.set_from_file("camorama.png")
	self.boton2.set_border_width(15)
	self.boton2.add(self.imagen2)
	self.boton2.set_tooltip_text("Este es el boton 2")
	self.boton3 = Gtk.Button()
	self.imagen3 = Gtk.Image()
	self.imagen3.set_from_file("flecha_arriba.png")
	self.boton3.set_border_width(15)
	self.boton3.add(self.imagen3)
	self.boton3.set_tooltip_text("Este es el boton 3")

	self.caja = Gtk.VBox()

	self.caja.pack_start(self.boton1,True,True,0)
	self.caja.pack_start(self.boton2,True,True,0)
	self.caja.pack_start(self.boton3,True,True,0)

        self.ventana.add(self.caja)
	self.ventana.show_all()
	self.ventana.connect("destroy", Gtk.main_quit)

    def main(self):
	Gtk.main()



if __name__ == "__main__":
    app = tabla()
    app.main()
