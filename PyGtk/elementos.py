#!/usr/bin/env python
import pygtk    # se importan las librerias gtk
pygtk.require('2.0')
import gtk
import os

class Base:
    def destroy(self, widget):
    	print "La ventana ha sido cerrado por un click"
        gtk.main_quit()
    def activar_inactivo(self, widget):
        self.boton_cambiante.get_active()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Elementos")
        self.window.set_size_request(500,700)
        self.window.set_border_width(10)

        self.separador = gtk.VSeparator()
        self.b6 = gtk.Button("Abrir")
        self.b6.set_border_width(8)

        self.texto = gtk.Entry()
        self.boton_cambiante = gtk.ToggleButton("Boton cambiante")
        self.boton_cambiante.connect("clicked", self.activar_inactivo)

        self.b2 = gtk.Button("Anterior") 
        self.b2.set_border_width(5)
        self.b3 = gtk.Button("Siguiente")
        self.b3.set_border_width(5)
        self.b4 = gtk.Button("Salir")
        self.b4.connect("clicked", self.destroy)
        self.b4.set_border_width(5)

        self.label = gtk.Label("Etiqueta 1")
        self.labelnumero = gtk.Label("Etiqueta 2 ")


        self.botones_activables = gtk.CheckButton("Botones activables ")
        self.botones_activables2 = gtk.CheckButton("Botones activables 2")


        self.solo_uno_activo = gtk.RadioButton(None ,"Opcion 1")
        self.solo_uno_activo2 = gtk.RadioButton(self.solo_uno_activo ,"Opcion 2")
        self.solo_uno_activo3 = gtk.RadioButton(self.solo_uno_activo ,"Opcion 3")

        self.barra_desplazamiento = gtk.HScrollbar()

        self.escala = gtk.HScale()
        self.escala.set_draw_value(True)
        self.escala.set_digits(8)
        self.escala.set_value_pos(10)

        self.imagen = gtk.Image()
        self.imagen.set_from_file("cartel-de-santa-vol-3.jpg")

        self.imagen_pixeles = gtk.Image()
        

        self.caja1 = gtk.HBox()
        self.caja1.pack_start(self.b2)
        self.caja1.pack_start(self.b3)
        self.caja1.pack_start(self.b4)
        
        self.caja2 = gtk.HBox()
        self.caja2.pack_start(self.texto)
        self.caja2.pack_start(self.separador)
        self.caja2.pack_start(self.b6)
        
        self.caja3 = gtk.HBox()
        self.caja3.pack_start(self.label)
        self.caja3.pack_start(self.labelnumero)
        self.caja3.pack_start(self.boton_cambiante)

        self.caja4 = gtk.HBox()
        self.caja4.pack_start(self.botones_activables)
        self.caja4.pack_start(self.botones_activables2)

        self.caja5 = gtk.VBox()
        self.caja5.pack_start(self.solo_uno_activo)
        self.caja5.pack_start(self.solo_uno_activo2)
        self.caja5.pack_start(self.solo_uno_activo3)

        self.caja6 = gtk.VBox()
        self.caja6.pack_start(self.barra_desplazamiento)
        self.caja6.pack_start(self.escala)

        self.caja7 = gtk.VBox()
        self.caja7.pack_start(self.imagen)

        self.caja = gtk.VBox()
        self.caja.pack_start(self.caja2)
        self.caja.pack_start(self.caja1)
        self.caja.pack_start(self.caja3)    
        self.caja.pack_start(self.caja4)
        self.caja.pack_start(self.caja5)
        self.caja.pack_start(self.caja6)
        self.caja.pack_start(self.caja7)
        
        self.window.add(self.caja)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)

    def main(self):
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
