#!/usr/bin/env python
import gtk, pygtk, cairo
pygtk.require('2.0')

class dibujar:
    def __init__(self):
	self.ventana = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.ventana.set_position(gtk.WIN_POS_CENTER)
	self.ventana.set_size_request(600,500)
	self.ventana.set_title("Dibujando un rectangulo")

	self.areaDibujo = gtk.DrawingArea()
	self.areaDibujo.connect("expose-event", self.dibujando)
	self.ventana.add(self.areaDibujo)
	self.ventana.connect("destroy", gtk.main_quit)
	self.ventana.show_all()


    def main(self):
	gtk.main()

    def dibujando(self, widget,areaDibujo ):
        self.style = self.areaDibujo.get_style()
	self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
        self.areaDibujo.window.draw_line(self.gc, 100,100 , 500, 350)

if __name__ == "__main__":
   objeto = dibujar()
   objeto.main()
