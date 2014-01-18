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
	self.ventana.connect( "motion_notify_event", self.moviendo)
	self.ventana.connect( "button_press_event", self.se_ha_dado_click)
	
 
    def main(self):
	gtk.main()

    def moviendo(self, event, widget):
	if gtk.gdk.BUTTON1_MASK == True:
	    print "el raton se ha movido"

    def se_ha_dado_click(self, event, widget):
	print "se ha dado click"



if __name__ == "__main__":
    aplicacion = editor()
    aplicacion.main()
