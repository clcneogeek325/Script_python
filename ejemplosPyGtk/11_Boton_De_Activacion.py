#!/usr/bin/env python
import gtk, pygtk
pygtk.require('2.0')

class tabla:
    def __init__(self):
	self.ventana = gtk.Window( gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position( gtk.WIN_POS_CENTER)
	self.ventana.set_title("Ejemplo de botones de Activacion")
	self.ventana.set_size_request(400,400)
	self.ventana.set_tooltip_text("Ejemplo sobloe botones activables")

	self.boton1 = gtk.CheckButton("Activaciion 1")
	self.boton1.connect("clicked", self.mensaje1)
	self.boton2 = gtk.CheckButton("Activaciion 2")
	self.boton2.connect("clicked", self.mensaje2)
	self.boton3 = gtk.CheckButton("Activaciion 3")
	self.boton3.connect("clicked", self.mensaje3)

	self.caja = gtk.VBox()

	self.caja.pack_start(self.boton1)
	self.caja.pack_start(self.boton2)
	self.caja.pack_start(self.boton3)

        self.ventana.add(self.caja)
	self.ventana.show_all()
	self.ventana.connect("destroy", gtk.main_quit)

    def main(self):
	gtk.main()

    def mensaje1(self, widget):
	estado =  widget.get_active()
	if estado == True:
	    print "El boton 1  esta pulsado"
	else:
	    print "El boton 1  no esta pulsado"
    def mensaje2(self, widget):
	estado =  widget.get_active()
	if estado == True:
	    print "El boton 2  esta pulsado"
	else:
	    print "El boton 2 no esta pulsado"
    def mensaje3(self, widget):
	estado =  widget.get_active()
	if estado == True:
	    print "El boton 3 esta pulsado"
	else:
	    print "El boton 3 no esta pulsado"



if __name__ == "__main__":
    app = tabla()
    app.main()
