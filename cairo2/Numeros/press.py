#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import threading
import time
import gobject
import gtk
import cairo

gobject.threads_init()

class MyThread(threading.Thread):
     def __init__(self, area):
         super(MyThread, self).__init__()
         self.area = area
         self.quit = False
	 self.counter = ""

     def dibujando1( self, area):
         ctx = self.area.window.cairo_create()
	 #fondo del dibujo
         ctx.set_source_rgb(1,1,1 ) # fondo azul
	 ctx.rectangle(0, 0, 300, 300)#tamanio del fondo
	 ctx.fill()

         # dibujando el texto
         ctx.select_font_face('Ubuntu')#definiendo la fuente de las letras
         ctx.set_font_size(250) # definiendo el tamanio de la fuente
  	 ctx.move_to(90, 230) # moviendo las letras hacien un punto
 	 ctx.set_source_rgb(.50, .90, 0) # letras amarillas
 	 ctx.show_text(str(self.counter))#mostrando el texto
  	 ctx.stroke() # commit to surface

     def run(self):
         while not self.quit:
	     for self.counter in range(0,11):
		 gobject.idle_add(self.dibujando1, self.counter)
		 time.sleep(1)
	     for self.counter in range(1,11):
		 self.counter =  10- self.counter
		 gobject.idle_add(self.dibujando1, self.counter)
		 time.sleep(1)
	     self.quit = True


w = gtk.Window(gtk.WINDOW_TOPLEVEL)
w.set_position(gtk.WIN_POS_CENTER)
w.set_size_request(300,300)
w.set_resizable(False)
area = gtk.DrawingArea()
w.add(area)
w.show_all()
w.connect("destroy",gtk.main_quit)

t = MyThread(area)
t.start()

gtk.main()
t.quit = True
