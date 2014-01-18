#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import threading
import time
import gobject
import os
import gtk
import cairo
from gtk import gdk
 
def expose_event(widget, event):
    cr = widget.window.cairo_create()
    size = widget.get_size()
 
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.rectangle(1, 1, size[0]-2, size[1]-2)
 
    cr.set_source_rgba(1, 1, 1, 0)
    cr.stroke_preserve()
 
    cr.set_source_rgba(1, 1, 1, 0)
    cr.fill()

def clicked(widget, event):
    ventana.begin_move_drag(event.button, int(event.x_root), int(event.y_root), event.time)



gobject.threads_init()

class MyThread(threading.Thread):
     def __init__(self, imagen):
         super(MyThread, self).__init__()
         self.imagen = imagen
         self.quit = False

     def update_label(self):
         self.imagen.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size(self.imagen, 340, 240))
         return False

     def run(self):
         while not self.quit:
             salida = os.popen('ls *.jpg *.png').read()        
             nombres = salida.split()
             
             for X in range(len(nombres)):
                    self.imagen.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size(nombres[X], 340, 240))
                    gobject.idle_add(self.update_label)
                    time.sleep(8)
  
    
ventana = gtk.Window()

ventana.set_size_request(350,210)
ventana.set_position(gtk.WIN_POS_MOUSE)
ventana.set_decorated(False)
ventana.set_app_paintable(True)
ventana.set_resizable(False)
ventana.set_size_request(340,240)
ventana.add_events(gdk.BUTTON_PRESS_MASK )
ventana.connect('button-press-event', clicked)
imagen = gtk.Image()
screen = ventana.get_screen()
colormap = screen.get_rgba_colormap()
ventana.set_colormap(colormap)

caja = gtk.VBox()
caja.pack_start(imagen)

ventana.add(caja)
ventana.show_all()
ventana.connect('delete-event', gtk.main_quit)
ventana.connect('expose-event', expose_event)
ventana.realize()
ventana.window.set_back_pixmap(None, False)

ventana.connect("destroy", lambda _: gtk.main_quit())
hilo = MyThread(imagen)
hilo.start()

gtk.main()
hilo.quit = True
