#!/usr/bin/env python
import threading
import gtk
import gobject
import time

def dibujar(numero, widget, event):
    ctx = widget.window.cairo_create()
    ctx.select_font_face('Arial Black')
    ctx.set_font_size(60) # em-square height is 90 pixels
    ctx.move_to(10, 90) # move to point (x, y) = (10, 90)
    ctx.set_source_rgb(1.00, 0.83, 0.00) # yellow
    ctx.show_text(str(numero))
    ctx.stroke()

gobject.threads_init()

class Contador(threading.Thread):
    def __init__(self, areaDibujo):
	super(Contador, self).__init__()
	self.l  = areaDibujo
	self.quit = False


    def run(self):
	numero = 0
	while not self.quit:
	    numero += 1
	    gobject.idle_add(self.dibujar, numero)
	    time.sleel(1)


w = gtk.Window()
l = gtk.DrawingArea()
l.connect("expose-event", self.dibujar)
w.add(l)
w.show_all()
w.connect("destroy", lambda _: gtk.main_quit())
t = MyThread(l)
t.start()

gtk.main()
t.quit = True
