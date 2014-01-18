#!/usr/bin/env python 
import pygtk
pygtk.require('2.0')
import gtk

class ejemlo2:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(500,100)
	self.ventana.set_title("Ejemplo de una etiqueta")
	self.ventana.set_tooltip_text("Tan solo escribe algo en el campo de texto para enviarlo ala etiqueta del final")

	self.boton = gtk.Button("Enviar")
	self.boton.connect("clicked", self.enviar_texto)

        self.etiqueta1 = gtk.Label("--------->  ")
        self.etiqueta2 = gtk.Label("etiqueta")

	self.entrada_texto = gtk.Entry()

	self.caja = gtk.HBox()
	self.caja.pack_start(self.entrada_texto)
	self.caja.pack_start(self.boton)
	self.caja.pack_start(self.etiqueta1)
	self.caja.pack_start(self.etiqueta2)

	self.ventana.add(self.caja)
	self.ventana.connect("destroy", gtk.main_quit)
	self.ventana.show_all()

    def main(self):
	gtk.main()

    def enviar_texto(self, widget):
	mensaje = self.entrada_texto.get_text()
	self.etiqueta2.set_text(mensaje)


if __name__ == "__main__":
    app = ejemlo2()
    app.main()


