#!/usr/bin/env python
import threading
import time
import gobject
import gtk
import os
import cairo

 
def expose_event(widget, event):
    cr = widget.window.cairo_create()
    size = widget.get_size()
 
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.rectangle(1, 1, size[0]-2, size[1]-2)
 
    cr.set_source_rgba(1, 1, 1, .8)
    cr.stroke_preserve()
 
    cr.set_source_rgba(1, 1, 1, .2)
    cr.fill()



gobject.threads_init()

class MyThread(threading.Thread):
     def __init__(self, imagen, archivo):
         super(MyThread, self).__init__()
         self.imagen = imagen
         self.archivo = archivo
         self.l = l
         self.texto = texto
         self.quit = False

     def update_label(self, widget, imagen, archivo):
         self.imagen.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size(self.imagen, 360, 160))
         return False

     def run(self):
         while not self.quit:
             salida = os.popen('ls *.jpg *.png').read()        
             nombres = salida.split()
             numero = int(self.l.get_text())
             
             if numero != len(nombres):
                if numero == 1:
                    self.imagen.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size(nombres[1], 360, 160))
                    self.texto.set_text(nombres[1])
                    archivo = self.l.set_text("2")
                    gobject.idle_add(self.update_label, archivo)
                    time.sleep(1)
                else:
                    self.imagen.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size(nombres[numero], 360, 160))
                    self.texto.set_text(nombres[numero])
                    archivo = self.l.set_text(str(numero + 1))
                    gobject.idle_add(self.update_label, archivo)
                    time.sleep(1)
             else:
                self.imagen.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size(nombres[1], 360, 160))
                self.l.set_text("0")       
                archivo = self.texto.set_text(nombres[0])
                gobject.idle_add(self.update_label, archivo)
                time.sleep(1)
    
ventana = gtk.Window()
ventana.set_size_request(400,230)

ventana.set_decorated(False)
ventana.set_app_paintable(True)
ventana.set_resizable(False)
        
l = gtk.Label("1")
imagen = gtk.Image()
imagen.set_size_request(360,160)
texto = gtk.Label()

screen = ventana.get_screen()
colormap = screen.get_rgba_colormap()
ventana.set_colormap(colormap)

archivo = ""

caja1 = gtk.HBox()
caja1.pack_start(texto)
caja1.pack_start(l)

caja = gtk.VBox()
caja.pack_start(caja1)
caja.pack_start(imagen)

ventana.add(caja)
ventana.show_all()
ventana.connect('delete-event', gtk.main_quit)
ventana.connect('expose-event', expose_event)
ventana.realize()
ventana.window.set_back_pixmap(None, False)

ventana.connect("destroy", lambda _: gtk.main_quit())
hilo = MyThread(imagen, archivo)
hilo.start()

gtk.main()
hilo.quit = True
