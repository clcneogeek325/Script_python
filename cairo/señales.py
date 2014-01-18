#!/usr/bin/env python
import pygtk, gtk
from gtk import gdk
pygtk.require('2.0')

class editor:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.ventana.set_position( gtk.WIN_POS_CENTER)
	self.ventana.set_title("Editor de Texo")	
	self.ventana.set_size_request(500, 400)

	self.ventana.show_all()
	self.ventana.add_events(gdk.ALL_EVENTS_MASK)
	self.ventana.connect("destroy", gtk.main_quit)
	self.ventana.connect("scroll_event", self.boton_central)
	self.ventana.connect("key_press_event", self.teclas)
	self.ventana.connect("button_press_event", self.un_click)
	#self.ventana.connect("scroll_event" self.doble_click)
	#self.ventana.connect("scroll_event" self.tres_clicks)
	#self.ventana.connect("button_release_event", self.despulando)
	self.ventana.connect("enter_notify_event", self.paseando_en_ventana)
	self.ventana.connect("focus_in_event", self.presionado_bar_titulo)
	#self.ventana.connect("", self.desconocido)
	
 
    def main(self):
	gtk.main()

    def desconocido(self, event, widget):
	print "evento desconocido"

    def presionado_bar_titulo(self, event, widget):
	print "clicke en la barra de titulo"

    def un_click(self, event, widget):
	print "se ha dado un click ala ventana"


    def doble_click(self, event, widget):
	print "se ha dado 2 clicks"


    def tres_clicks(self, event, widget):
	print "se ha dado 3 clicks"

    def teclas(self, event, widget):
	print "se ha presionado una tecla"

    def boton_central(self, event, widget):
	print "se han rotado el boton central"

    def paseando_en_ventana(self, event, widget):
	print "El raton se ha paseado por la ventana"

  # def despulando(self, event, widget):
   #	print " este evento se activa cuando se da u
   #	n click y se suelta el boton del mouse button_release_event"


if __name__ == "__main__":
    aplicacion = editor()
    aplicacion.main()
