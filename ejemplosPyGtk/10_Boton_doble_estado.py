#!/usr/bin/env python
import gtk, pygtk
pygtk.require('2.0')

class tabla:
    def __init__(self):
	self.ventana = gtk.Window( gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position( gtk.WIN_POS_CENTER)
	self.ventana.set_title("Ejemplo de una tabla")
	self.ventana.set_size_request(400,400)
	self.ventana.set_tooltip_text("Ejemplo sobloe botones activables")

	self.etiqueta = gtk.Label("Pulsa un boton")
	self.boton2 = gtk.ToggleButton("Boton1")
	self.boton2.connect("clicked", self.mensaje)
	self.boton3 = gtk.ToggleButton("Boton2")
	self.boton3.connect("clicked", self.mensaje)

	self.caja = gtk.VBox()

	self.caja.pack_start(self.etiqueta)
	self.caja.pack_start(self.boton2)
	self.caja.pack_start(self.boton3)

        self.ventana.add(self.caja)
	self.ventana.show_all()
	self.ventana.connect("destroy", gtk.main_quit)

    def main(self):
	gtk.main()

    def mensaje(self, widget):
	estado =  widget.get_active()
	if estado == True:
	    print "El boton esta pulsado"
	else:
	    print "El boton no esta pulsado"



if __name__ == "__main__":
    app = tabla()
    app.main()
