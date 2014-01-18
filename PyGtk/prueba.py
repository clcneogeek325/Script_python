#!/usr/bin/env python
import pygtk    # se importan las librerias gtk
pygtk.require('2.0')
import gtk
import os
import threading, time


gtk.gdk.threads_init()

class Base:
    def siguiente(self, widget):
        salida = os.popen('ls *.jpg *.png').read()        
        nombres = salida.split()
        numero = int(self.labelnumero.get_text())
        
        if numero != len(nombres):
            if numero == 1:
               self.imagen.set_from_file(nombres[1])
               self.texto.set_text(nombres[1])
               self.labelnumero.set_text("2")
            else:
               self.imagen.set_from_file(nombres[numero])
               self.texto.set_text(nombres[numero])
               self.labelnumero.set_text(str(numero + 1))
        else:
            self.imagen.set_from_file(nombres[1])
            self.labelnumero.set_text("0")       
            self.texto.set_text(nombres[0])
    def anterior(self, widget):
        salida = os.popen('ls *.jpg *.png').read()
        nombres = salida.split()
        numero = int(self.labelnumero.get_text())

        if numero != 0:
            self.texto.set_text(nombres[numero - 1])
            self.imagen.set_from_file(nombres[numero - 1])
            self.labelnumero.set_text(str(numero - 1))
        else:
            self.labelnumero.set_text(str(len(nombres)))
            self.texto.set_text(nombres[numero])

    def destroy(self, widget):
    	print "La ventana ha sido cerrado por un click"
        gtk.main_quit()

    def abrir(self, widget):
        dialogo = gtk.FileChooserDialog("Seleccione la imagen",
               None, gtk.FILE_CHOOSER_ACTION_OPEN,
               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
               gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialogo.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("Imagenes")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.jpeg")
        dialogo.add_filter(filter)

        response = dialogo.run()
        if response == gtk.RESPONSE_OK:
            self.imagen.set_from_file(dialogo.get_filename())
            dialogo.destroy()
        elif response == gtk.RESPONSE_CANCEL:
            print "No se ha selecionado niguna mimagen"
            raise SystemExit
            dialogo.destroy()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Slayder")
        self.window.set_size_request(1000, 700)
        self.window.set_border_width(10)

        self.separador = gtk.VSeparator()
        self.b6 = gtk.Button("Abrir")
        self.b6.set_tooltip_text("Da click este boton si quieres abrir una imagen de otra carpeta")
        self.b6.connect("clicked", self.abrir)
        self.b6.set_border_width(8)

        self.texto = gtk.Entry()

        self.b2 = gtk.Button("Anterior") 
        self.b2.connect("clicked", self.anterior)
        self.b2.set_border_width(5)
        self.b3 = gtk.Button("Siguiente")
        self.b3.connect("clicked", self.siguiente)
        self.b3.set_border_width(5)
        self.b4 = gtk.Button("Salir")
        self.b4.connect("clicked", self.destroy)
        self.b4.set_border_width(5)
        self.b5 = gtk.Button("Automatico")
        self.b5.connect("clicked", self.imprimir)

        self.label = gtk.Label("Imagen numero :")
        self.labelnumero = gtk.Label("1")
        
        self.separador2 = gtk.VSeparator()

        self.imagen = gtk.Image()
        self.imagen.set_from_file("look-image.jpg")
        self.imagen.set_size_request(500,500)

        self.caja1 = gtk.HBox()
        self.caja1.pack_start(self.b6)
        self.caja1.pack_start(self.b2)
        self.caja1.pack_start(self.b3)
        self.caja1.pack_start(self.b5)
        self.caja1.pack_start(self.b4)
        
        self.caja2 = gtk.HBox()
        self.caja2.pack_start(self.separador2)
        self.caja2.pack_start(self.texto)
        self.caja2.pack_start(self.separador)
        
        self.caja3 = gtk.HBox()
        self.caja3.pack_start(self.label)
        self.caja3.pack_start(self.labelnumero)

        self.caja = gtk.VBox()
        self.caja.pack_start(self.caja2)
        self.caja.pack_start(self.caja1)
        self.caja.pack_start(self.caja3)
        self.caja.pack_start(self.imagen)
        
        self.window.add(self.caja)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)

    def imprimir(self, widget):
	gtk.gdk.threads_enter()
        while True:
            salida = os.popen('ls *.jpg *.png').read()        
            nombres = salida.split()
            numero = int(self.labelnumero.get_text())
            if numero != len(nombres):
                if numero == 1:
                    self.imagen.set_from_file(nombres[1])
                    self.texto.set_text(nombres[1])
                    self.labelnumero.set_text("2")
                    time.sleep(1)
                else:
                    self.imagen.set_from_file(nombres[numero])
                    self.texto.set_text(nombres[numero])
                    self.labelnumero.set_text(str(numero + 1))
                    time.sleep(1)
            else:
                self.imagen.set_from_file(nombres[1])
                self.labelnumero.set_text("0")       
                self.texto.set_text(nombres[0])
                time.sleep(1)
        gtk.gdk.threads_leave()

    def click(self, event):
	



    def main(self):
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
