#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
import pygtk    # se importan las librerias gtk
pygtk.require('2.0')
import gtk

class Base: # se define la clase Base
    global imagen
    def destroy(self, widget, data=None):#se crea un metodo para cerrar la vetana o el proceso
	print "La ventana ha sido cerrado por un click"
          gtk.main_quit(False)


    def cambiar_imagen(self, widget):
        self.imagen.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size("Pallazo.png", 500, 300))

    def __init__(self):# el metodo que tendra la ventana
        self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.ventana.set_position(gtk.WIN_POS_CENTER)#posicion 
        self.ventana.set_size_request(600, 600)#las dimensiones de la ventana


        self.ventana.set_title("Mi primer interface Gtk en python")

        self.botton1 = gtk.Button("Salir")
        self.botton1.connect("clicked", self.destroy)
        self.botton1.set_tooltip_text("Al dar click en este boton la aplicasion ce cerrar")

        self.botton2 = gtk.Button("Esconder")
 
        self.botton3 = gtk.Button("mostrar")
 
 
        self.texto = gtk.Entry()
        self.texto.set_tooltip_text("Al escribir en el cuadro de texto se cambiara el titulo") 
            
        self.botton4 = gtk.Button("relabel")
       
        self.boton5 = gtk.Button("Cambiar imagen")
        self.boton5.connect("clicked", self.cambiar_imagen)

        self.boton6 = gtk.Button("Adicionar a combo")
       
        self.label1 = gtk.Label("new label")

        
   
        
        self.imagen = gtk.Image()
        self.imagen.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size("look-image.jpg", 500, 300))

        self.box1 = gtk.HBox()
        self.box1.pack_start(self.botton1)
        self.box1.pack_start(self.botton2)
        self.box1.pack_start(self.botton3)
        self.box1.pack_start(self.botton4)
        self.box1.pack_start(self.boton5)
         
        self.box3 = gtk.HBox()
        self.box3.pack_start(self.texto)
        self.box3.pack_start(self.boton6)
      
        self.box2 = gtk.VBox()
        self.box2.pack_start(self.box1)
        self.box2.pack_start(self.label1)
        self.box2.pack_start(self.box3)
        self.box2.pack_start(self.imagen)

        self.ventana.add(self.box2)#se adiciona el box ala ventana
        self.ventana.show_all()#muestra la ventana
        self.ventana.connect("destroy", self.destroy)

    def main(self):#es el metodo main
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
 
